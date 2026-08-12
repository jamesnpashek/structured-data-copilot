KNOWN_TYPES = {"Article", "Product", "FAQPage", "Organization", "LocalBusiness",
               "Event", "Recipe", "Review", "BreadcrumbList", "VideoObject"}


def normalize(page_text: str, existing_jsonld: list[dict]) -> dict:
    """Identify schema types present and clean up the page content."""
    detected_types = []
    for block in existing_jsonld:
        t = block.get("@type")
        if isinstance(t, list):
            detected_types.extend(t)
        elif isinstance(t, str):
            detected_types.append(t)

    # Infer from page text if no existing markup
    if not detected_types:
        detected_types = _infer_types(page_text)

    return {
        "text": page_text[:8000],
        "schema_types": list(set(detected_types) & KNOWN_TYPES) or ["Article"],
        "existing_jsonld": existing_jsonld,
    }


def _infer_types(text: str) -> list[str]:
    lower = text.lower()
    types = []
    if "faq" in lower or "frequently asked" in lower:
        types.append("FAQPage")
    if "$" in text or "price" in lower or "buy" in lower:
        types.append("Product")
    if not types:
        types.append("Article")
    return types
