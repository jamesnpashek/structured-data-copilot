from validate.google_rules import check_google_rules
from validate.schema_org import check_schema_org


def validate(jsonld: dict) -> dict:
    """Run both schema.org conformance and Google rich-results checks."""
    errors = []
    warnings = []

    schema_result = check_schema_org(jsonld)
    errors.extend(schema_result["errors"])
    warnings.extend(schema_result["warnings"])

    google_result = check_google_rules(jsonld)
    errors.extend(google_result["errors"])
    warnings.extend(google_result["warnings"])

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "schema_type": jsonld.get("@type"),
    }
