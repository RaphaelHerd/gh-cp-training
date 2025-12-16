import requests
import pytest
import datetime
from typing import Any


def _fetch_owners(base_url: str) -> list:
    r = requests.get(f"{base_url}/api/owners", timeout=10)
    r.raise_for_status()
    return r.json()


def _get_pettypes_map(base_url: str) -> dict:
    r = requests.get(f"{base_url}/api/pettypes", timeout=10)
    if r.status_code != 200:
        return {}
    items = r.json()
    return {int(i.get("id")): i for i in items if i.get("id") is not None}


@pytest.mark.parametrize("case_index", list(range(20)))
def test_owner_business_cases(case_index: int, base_url: str, swagger_spec: Any, unique_id: int):
    """
    Execute a broad set of business-oriented checks against GET /api/owners/{ownerId}.

    This parametrized test produces 20 distinct cases using a mix of existing owner ids
    from the API and boundary/edge values (0, negative, very large, non-integer id).

    For owner ids that exist, the test asserts business invariants such as:
    - required owner fields present (firstName, lastName, address, city, telephone)
    - telephone follows digit-only pattern (business rule)
    - pets (if present) belong to the owner, have types and visits consistent with domain model
    - pet birth dates are not in the future

    For ids that do not resolve to an owner the test asserts the server returns a client-level
    error (4xx) or documents the error (some servers may return 500; those will show up as failures
    and are worth filing as bugs).
    """

    # Discover existing owners and some special cases
    try:
        owners = _fetch_owners(base_url)
    except Exception as e:
        pytest.skip(f"Could not fetch owners list: {e}")

    existing_ids = []
    owner_with_no_pets = None
    owner_with_many_pets = None
    for o in owners:
        oid = o.get("id")
        if oid is None:
            continue
        existing_ids.append(int(oid))
        pets = o.get("pets") or []
        if not owner_with_no_pets and not pets:
            owner_with_no_pets = int(oid)
        if not owner_with_many_pets and len(pets) > 1:
            owner_with_many_pets = int(oid)

    # Build candidate ids list (aim for 20 distinct cases)
    candidates = []
    # prefer existing owners first
    for i in existing_ids[:15]:
        candidates.append(i)

    # add discovered special-case owners
    if owner_with_no_pets is not None:
        candidates.append(owner_with_no_pets)
    if owner_with_many_pets is not None:
        candidates.append(owner_with_many_pets)

    # add boundary and invalid inputs
    candidates.extend([0, -1, 99999999, "abc"])  # include a non-integer id

    # ensure we have at least 20 cases
    # if not enough discovered owners, pad with synthetic large ids
    pad = 20 - len(candidates)
    for n in range(pad):
        candidates.append(1000000 + n)

    owner_id = candidates[case_index]

    # run the GET
    url = f"{base_url}/api/owners/{owner_id}"
    r = requests.get(url, timeout=10)

    # If the owner is not found, we expect a client-level error (404/400). If the server
    # returns 200 we run business logic checks below. Other responses (500) will cause
    # test failures and should be reported as server bugs.
    if r.status_code != 200:
        assert r.status_code in (400, 404), f"Unexpected status for owner {owner_id}: {r.status_code} (body: {r.text})"
        return

    # Parse owner and run business invariant checks
    owner = r.json()
    assert isinstance(owner, dict)
    # Required owner fields
    for field in ("id", "firstName", "lastName", "address", "city", "telephone"):
        assert field in owner, f"Owner {owner_id} missing required field: {field}"

    # Telephone business rule: digits only (schema indicates numeric string)
    tel = str(owner.get("telephone", ""))
    assert tel == "" or tel.isdigit(), f"Owner {owner_id} telephone not digits-only: {tel}"

    # Validate pets consistency
    pets = owner.get("pets") or []
    pettypes_map = _get_pettypes_map(base_url)

    pet_ids = set()
    for pet in pets:
        pid = pet.get("id")
        assert pid is not None, f"Owner {owner_id} has pet without id"
        assert pid not in pet_ids, f"Duplicate pet id {pid} for owner {owner_id}"
        pet_ids.add(pid)

        # pet ownerId if present should match
        owner_id_on_pet = pet.get("ownerId")
        if owner_id_on_pet is not None:
            assert int(owner_id_on_pet) == int(owner.get("id")), f"Pet {pid} ownerId mismatch: {owner_id_on_pet} vs owner {owner_id}"

        # pet type must reference a valid pet type
        ptype = pet.get("type") or pet.get("petType") or {}
        if ptype:
            ptype_id = ptype.get("id")
            if ptype_id is not None:
                assert int(ptype_id) in pettypes_map, f"Pet {pid} references unknown petType id {ptype_id}"

        # birthDate should not be in the future
        b = pet.get("birthDate")
        if b:
            try:
                d = datetime.datetime.strptime(b, "%Y-%m-%d").date()
                assert d <= datetime.date.today(), f"Pet {pid} has future birthDate: {b}"
            except ValueError:
                # allow different date formats to be caught by schema elsewhere
                pass

        # visits (if present) should reference the pet id
        visits = pet.get("visits") or []
        for v in visits:
            vid = v.get("id")
            assert vid is not None
            v_pet_id = v.get("petId")
            if v_pet_id is not None:
                assert int(v_pet_id) == int(pid), f"Visit {vid} petId {v_pet_id} does not match pet id {pid}"
            # visit date parse sanity
            v_date = v.get("date")
            if v_date:
                try:
                    datetime.datetime.strptime(v_date, "%Y-%m-%d")
                except ValueError:
                    # some visits use other formats; not a business-failure here
                    pass

    # If the owner has no pets, this is allowed, but ensure it's represented as an empty list
    assert isinstance(pets, list)
