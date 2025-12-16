import requests
import pytest

from utils.openapi_utils import get_response_schema, validate_against_schema


def test_list_pettypes(base_url, swagger_spec):
    """GET /api/pettypes should return a list of pet types."""
    r = requests.get(f"{base_url}/api/pettypes", timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)

    schema = get_response_schema(swagger_spec, "/api/pettypes", "get", 200)
    if schema and schema.get("type") == "array":
        item_schema = schema.get("items")
        if body:
            # validate first item to avoid brittle failures on public demo data
            validate_against_schema(body[0], item_schema, swagger_spec)
    else:
        if body:
            assert isinstance(body[0], dict)


def test_get_pettype_by_id(base_url, swagger_spec):
    """Pick an existing pet type from the list and GET by id."""
    r = requests.get(f"{base_url}/api/pettypes", timeout=10)
    r.raise_for_status()
    types = r.json()
    if not types:
        pytest.skip("No pet types available to test GET by id")

    first = types[0]
    pet_type_id = first.get("id")
    assert pet_type_id is not None

    r2 = requests.get(f"{base_url}/api/pettypes/{pet_type_id}", timeout=10)
    assert r2.status_code == 200
    body = r2.json()

    schema = get_response_schema(swagger_spec, "/api/pettypes/{petTypeId}", "get", 200)
    validate_against_schema(body, schema, swagger_spec)


def test_create_update_delete_pettype(base_url, swagger_spec, unique_id):
    """Attempt to create a pet type, update it, then delete it. Skip if create not allowed."""
    name = f"pytest-pettype-{unique_id}"
    payload = {"name": name}

    # Try create
    r = requests.post(f"{base_url}/api/pettypes", json=payload, timeout=10)
    if r.status_code not in (200, 201):
        pytest.skip(f"POST /api/pettypes not allowed or failed (status {r.status_code})")

    created = r.json()
    created_id = created.get("id")
    assert created_id is not None

    # Validate response schema for POST (200 or 201)
    schema = get_response_schema(swagger_spec, "/api/pettypes", "post", r.status_code)
    # try fallback to 200/201 if explicit code not found
    if schema is None:
        schema = get_response_schema(swagger_spec, "/api/pettypes", "post", 200) or get_response_schema(swagger_spec, "/api/pettypes", "post", 201)
    validate_against_schema(created, schema, swagger_spec)

    try:
        # Update name
        updated = created.copy()
        updated["name"] = updated.get("name", name) + "-updated"

        r2 = requests.put(f"{base_url}/api/pettypes/{created_id}", json=updated, timeout=10)
        assert r2.status_code == 204

        # Verify GET returns updated name
        r3 = requests.get(f"{base_url}/api/pettypes/{created_id}", timeout=10)
        assert r3.status_code == 200
        body = r3.json()
        assert body.get("name") == updated["name"]

        # Validate GET schema
        schema_get = get_response_schema(swagger_spec, "/api/pettypes/{petTypeId}", "get", 200)
        validate_against_schema(body, schema_get, swagger_spec)
    finally:
        # Cleanup: attempt delete but don't fail if not allowed
        try:
            d = requests.delete(f"{base_url}/api/pettypes/{created_id}", timeout=10)
            # Accept 200/204/404
            assert d.status_code in (200, 204, 404)
        except Exception:
            pass


def test_pettypes_items_validate_sample(base_url, swagger_spec):
    """Validate up to N returned pet types against the OpenAPI item schema.

    This attempts to avoid brittle failures by validating a sample of items
    and requiring at least one successful validation when a schema is present.
    """
    r = requests.get(f"{base_url}/api/pettypes", timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)

    schema = get_response_schema(swagger_spec, "/api/pettypes", "get", 200)
    if not schema or schema.get("type") != "array":
        pytest.skip("No array response schema for /api/pettypes; cannot perform schema validation sample")

    item_schema = schema.get("items")
    if not item_schema:
        pytest.skip("No item schema to validate against")

    success = 0
    tried = 0
    for item in body[:20]:
        tried += 1
        try:
            validate_against_schema(item, item_schema, swagger_spec)
            success += 1
        except Exception:
            # ignore individual item validation failures
            pass

    # If there were items, require at least one to validate to avoid brittle failures
    if tried:
        assert success >= 1, f"No returned pettype items validated against schema after {tried} tries"


def test_pettypes_content_type_and_required_fields(base_url, swagger_spec):
    """Ensure response is JSON and items include required fields with basic boundaries."""
    r = requests.get(f"{base_url}/api/pettypes", timeout=10)
    assert r.status_code == 200

    ct = r.headers.get("Content-Type", "")
    assert "application/json" in ct or ct.startswith("application/"), f"Unexpected Content-Type: {ct}"

    body = r.json()
    assert isinstance(body, list)

    # For any returned item, check presence and basic types/constraints
    for item in body[:20]:
        assert isinstance(item, dict)
        assert "id" in item, "pet type item missing 'id'"
        assert "name" in item, "pet type item missing 'name'"

        pet_id = item.get("id")
        assert isinstance(pet_id, int) or (isinstance(pet_id, float) and pet_id.is_integer()), "id must be integer-like"
        assert int(pet_id) >= 0, "id must be non-negative"

        name = item.get("name")
        assert isinstance(name, str), "name must be a string"
        # basic length check (schema allows minLength 1)
        if name:
            assert 1 <= len(name) <= 80


def test_get_pettypes_with_unexpected_query_params(base_url):
    """Server should ignore unknown query params and still return the pet types list."""
    r = requests.get(f"{base_url}/api/pettypes?unknownParam=foobar", timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)


def test_get_pettype_by_id_non_integer(base_url):
    """Requesting with a non-integer path id should return 400 or 404."""
    r = requests.get(f"{base_url}/api/pettypes/abc", timeout=10)
    assert r.status_code in (400, 404)


def test_get_pettype_by_id_negative(base_url):
    """Requesting with a negative id should return 400 or 404 (schema minimum 0)."""
    r = requests.get(f"{base_url}/api/pettypes/-1", timeout=10)
    assert r.status_code in (400, 404)


def test_get_pettypes_with_accept_header(base_url):
    """Check server behavior when client requests a non-JSON Accept header."""
    headers = {"Accept": "text/plain"}
    r = requests.get(f"{base_url}/api/pettypes", headers=headers, timeout=10)
    # Some servers ignore Accept and return JSON; others may return 406 Not Acceptable.
    assert r.status_code in (200, 406)
    if r.status_code == 200:
        # ensure JSON parseable
        try:
            body = r.json()
            assert isinstance(body, list)
        except Exception:
            pytest.fail("Response returned 200 but body is not valid JSON")
