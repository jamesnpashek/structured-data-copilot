import json
from bs4 import BeautifulSoup


def extract(html: str) -> tuple[str, list[dict]]:
    """Return (page_text, existing_jsonld_blocks)."""
    soup = BeautifulSoup(html, "html.parser")

    existing = []
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            existing.append(json.loads(tag.string or "{}"))
        except json.JSONDecodeError:
            pass

    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    lines = [l.strip() for l in soup.get_text(separator="\n").splitlines() if l.strip()]
    return "\n".join(lines), existing
