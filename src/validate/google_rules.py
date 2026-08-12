# Required and recommended properties per Google's rich results documentation.
# https://developers.google.com/search/docs/appearance/structured-data

REQUIRED: dict[str, list[str]] = {
    "Article": ["headline", "author", "datePublished"],
    "Product": ["name", "offers"],
    "FAQPage": ["mainEntity"],
    "Organization": ["name", "url"],
    "LocalBusiness": ["name", "address"],
    "Event": ["name", "startDate", "location"],
    "Recipe": ["name", "recipeIngredient", "recipeInstructions"],
}

RECOMMENDED: dict[str, list[str]] = {
    "Article": ["image", "dateModified", "description"],
    "Product": ["image", "description", "brand", "aggregateRating"],
    "FAQPage": [],
    "Organization": ["logo", "contactPoint", "sameAs"],
}


def check_google_rules(jsonld: dict) -> dict:
    schema_type = jsonld.get("@type", "")
    if isinstance(schema_type, list):
        schema_type = schema_type[0]

    errors, warnings = [], []

    for prop in REQUIRED.get(schema_type, []):
        if prop not in jsonld:
            errors.append(f"Missing required property for {schema_type}: '{prop}'")

    for prop in RECOMMENDED.get(schema_type, []):
        if prop not in jsonld:
            warnings.append(f"Missing recommended property for {schema_type}: '{prop}'")

    return {"errors": errors, "warnings": warnings}
