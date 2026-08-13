KNOWN_TYPES = {"Article", "Product", "FAQPage", "Organization", "LocalBusiness",
               "Event", "Recipe", "Review", "BreadcrumbList", "VideoObject"}

# LocalBusiness subtypes — map to LocalBusiness for retrieval purposes
_LOCAL_SUBTYPES = {
    "bakery", "cafe", "restaurant", "coffee", "bistro", "bar", "pub",
    "salon", "spa", "gym", "clinic", "dental", "pharmacy", "hotel",
    "store", "shop", "boutique", "gallery", "studio", "agency",
}

_LOCAL_SIGNALS = {
    "hours", "open", "closed", "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "sunday",
    "address", "location", "directions", "visit us", "find us",
    "phone", "call us", "reservations", "dine in", "takeout",
    "order online", "delivery", "menu", "catering",
}


def normalize(page_text: str, existing_jsonld: list[dict], url: str = "") -> dict:
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
        "url": url,
        "text": page_text[:8000],
        "schema_types": list(set(detected_types) & KNOWN_TYPES) or ["Article"],
        "existing_jsonld": existing_jsonld,
    }


def _infer_types(text: str) -> list[str]:
    lower = text.lower()
    types = []

    # FAQPage — check first, can coexist with others
    if "faq" in lower or "frequently asked" in lower:
        types.append("FAQPage")

    # LocalBusiness — check before Product; "$" appears on many local biz pages
    is_local = any(sig in lower for sig in _LOCAL_SUBTYPES)
    signal_count = sum(1 for sig in _LOCAL_SIGNALS if sig in lower)
    if is_local or signal_count >= 2:
        types.append("LocalBusiness")
    elif "recipe" in lower or "ingredients" in lower or "servings" in lower:
        types.append("Recipe")
    elif any(w in lower for w in ("add to cart", "add to bag", "buy now", "checkout", "sku", "in stock")):
        # Only Product if it looks like an actual product listing page, not just a page with prices
        types.append("Product")
    elif "event" in lower and any(w in lower for w in ("ticket", "register", "venue", "attend")):
        types.append("Event")

    # Fallback
    if not types:
        types.append("Article")

    return types
