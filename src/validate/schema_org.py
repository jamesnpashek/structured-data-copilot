REQUIRED_GLOBALS = ["@context", "@type"]


def check_schema_org(jsonld: dict) -> dict:
    errors, warnings = [], []

    for prop in REQUIRED_GLOBALS:
        if prop not in jsonld:
            errors.append(f"Missing required global property: '{prop}'")

    ctx = jsonld.get("@context", "")
    if ctx and "schema.org" not in str(ctx):
        errors.append("@context must reference schema.org")

    return {"errors": errors, "warnings": warnings}
