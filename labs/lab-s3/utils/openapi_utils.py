"""
Utilities to work with OpenAPI/Swagger specs for runtime schema validation.

This helper supports both OpenAPI v2 (swagger 2.0) and OpenAPI v3+ specs. It lets tests
extract response schemas for operations and validate JSON responses using jsonschema
with the spec as the reference store for $ref resolution.
"""
from typing import Any, Dict, Optional
import jsonschema


def get_response_schema(spec: Dict[str, Any], path: str, method: str, status_code: int) -> Optional[Dict[str, Any]]:
    """Return the JSON Schema (swagger schema) for the response of an operation.

    spec: full swagger.json loaded as dict
    path: path as declared in the spec (e.g. '/pet/{petId}')
    method: HTTP method name (e.g. 'get', 'post')
    status_code: numeric status code (e.g. 200)
    """
    paths = spec.get("paths", {})
    path_item = paths.get(path)
    if not path_item:
        return None
    op = path_item.get(method.lower())
    if not op:
        return None
    responses = op.get("responses", {})
    # responses keys are strings like "200", "default"
    resp = responses.get(str(status_code)) or responses.get("default")
    if not resp:
        # fallback: pick first response found
        for r in responses.values():
            resp = r
            break
    if not resp:
        return None
    # OpenAPI v3 stores schemas under content -> <media-type> -> schema
    content = resp.get("content")
    if content and isinstance(content, dict):
        # pick first media-type's schema if present
        for mt, mt_obj in content.items():
            schema = mt_obj.get("schema") if isinstance(mt_obj, dict) else None
            if schema:
                return schema
    # Fallback for OpenAPI v2 / swagger: schema is directly under the response
    return resp.get("schema")


def validate_against_schema(instance: Any, schema: Dict[str, Any], spec: Dict[str, Any]) -> None:
    """Validate a JSON instance against a schema fragment from the spec.

    This uses jsonschema and sets the spec as the resolution scope so $ref like "#/definitions/Pet"
    resolve correctly.
    """
    if schema is None:
        # nothing to validate against
        return

    # jsonschema's RefResolver.from_schema builds a resolver that can resolve internal refs
    try:
        resolver = jsonschema.RefResolver.from_schema(spec)
    except Exception:
        # Fallback: no resolver
        resolver = None

    # Perform validation (this raises jsonschema.exceptions.ValidationError on failure)
    if resolver is not None:
        jsonschema.validate(instance=instance, schema=schema, resolver=resolver)
    else:
        jsonschema.validate(instance=instance, schema=schema)
