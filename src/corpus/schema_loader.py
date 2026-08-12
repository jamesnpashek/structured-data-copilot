"""
Fetches schema.org property definitions for each supported type.
Uses the static HTML pages — they're server-rendered, no JS needed.
"""

import httpx
from bs4 import BeautifulSoup

SCHEMA_TYPES = [
    "Article", "Product", "FAQPage", "Organization",
    "LocalBusiness", "Event", "Recipe", "BreadcrumbList",
]

HEADERS = {"Accept": "text/html", "User-Agent": "structured-data-copilot/0.1"}


def load_schema_docs() -> list[dict]:
    """Return a list of {schema_type, source, text} dicts."""
    docs = []
    with httpx.Client(timeout=15, follow_redirects=True, headers=HEADERS) as client:
        for schema_type in SCHEMA_TYPES:
            url = f"https://schema.org/{schema_type}"
            try:
                resp = client.get(url)
                resp.raise_for_status()
                text = _parse_type_page(resp.text, schema_type)
                if text:
                    docs.append({"schema_type": schema_type, "source": url, "text": text})
                    print(f"  [schema.org] {schema_type}: {len(text)} chars")
            except Exception as e:
                print(f"  [schema.org] WARN {schema_type}: {e}")
    return docs


def _parse_type_page(html: str, schema_type: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    lines = [f"schema.org/{schema_type} — Property Definitions\n"]

    # schema.org renders property rows as <tr> inside a <table class="definition-table">
    for table in soup.find_all("table", class_="definition-table"):
        for row in table.find_all("tr"):
            cells = row.find_all(["th", "td"])
            if len(cells) < 3:
                continue
            prop = cells[0].get_text(" ", strip=True)
            expected = cells[1].get_text(" ", strip=True)
            desc = cells[2].get_text(" ", strip=True)
            if prop and desc:
                lines.append(f"- {prop} (type: {expected}): {desc}")

    # Also grab the top-level description of the type itself
    desc_el = soup.find("div", class_="dctype") or soup.find("meta", {"name": "description"})
    if desc_el:
        type_desc = (desc_el.get("content") or desc_el.get_text(strip=True))[:300]
        lines.insert(1, f"Description: {type_desc}\n")

    return "\n".join(lines)
