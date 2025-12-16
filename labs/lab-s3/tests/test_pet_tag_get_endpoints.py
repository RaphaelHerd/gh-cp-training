"""Tests that exercise all GET operations tagged 'pet' in the OpenAPI spec.

This test discovers GET endpoints tagged with 'pet' and issues requests against
the server described in the OpenAPI `servers[0].url`.

For operations requiring path parameters (ownerId, petId) the test uses the
`created_owner` and `created_pet` fixtures to provide valid ids.

These tests intentionally avoid strict schema validation and focus on
existence/availability of the endpoints and JSON parseability for 200 responses.
"""
import requests
import pytest
from typing import Optional


def _substitute_path(path: str, owner_id: Optional[int], pet_id: Optional[int]) -> Optional[str]:
    p = path
    if "{petId}" in p:
        if pet_id is None:
            return None
        p = p.replace("{petId}", str(pet_id))
    if "{ownerId}" in p:
        if owner_id is None:
            return None
        p = p.replace("{ownerId}", str(owner_id))
    # If any other template variables remain, we can't call it
    if "{" in p:
        return None
    return p


def test_all_get_pet_endpoints(swagger_spec, base_url, created_owner, created_pet):
    paths = swagger_spec.get("paths", {})

    owner_id = created_owner.get("id") if created_owner else None
    pet_id = created_pet.get("id") if created_pet else None

    # collect GET endpoints that appear to be pet-related. The original tests
    # relied on a tag named 'pet' and the old /pet paths; the new API exposes
    # pet resources under /api/pets and may use different tagging. To be robust
    # discover operations by either tag or path name containing 'pet'.
    pet_get_ops = []
    for path, path_item in paths.items():
        for method, op in path_item.items():
            if method.lower() != "get":
                continue
            tags = op.get("tags", []) or []
            path_l = path.lower()
            if any(("pet" in (t.lower() if isinstance(t, str) else "") for t in tags)) or "pet" in path_l:
                pet_get_ops.append((path, op))

    # If there are no discovered pet endpoints, skip the test instead of failing
    # (the API may not expose 'pet' resources in a way this test recognizes).
    if not pet_get_ops:
        pytest.skip("No GET pet-related operations found in spec")

    failures = []
    for path, op in pet_get_ops:
        call_path = _substitute_path(path, owner_id, pet_id)
        if not call_path:
            # skip endpoints we cannot call due to unknown parameters
            continue

        url = f"{base_url}{call_path}"
        try:
            r = requests.get(url, timeout=10)
        except Exception as exc:
            failures.append((url, f"request-failed: {exc}"))
            continue

        if r.status_code == 200:
            # ensure JSON parseable when returning 200 with JSON content
            ct = r.headers.get("Content-Type", "")
            if "application/json" in ct or ct.startswith("application/"):
                try:
                    r.json()
                except Exception as exc:
                    failures.append((url, f"invalid-json: {exc}"))
        elif r.status_code in (204, 201, 304):
            # Acceptable success-like responses for some endpoints
            pass
        else:
            failures.append((url, f"unexpected-status: {r.status_code}"))

    assert not failures, f"Some pet GET endpoints failed: {failures}"
