"""
Fetches Google's rich results eligibility documentation.
Uses Playwright because developers.google.com is JS-rendered.
"""

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

GOOGLE_DOCS: dict[str, str] = {
    "Article":       "https://developers.google.com/search/docs/appearance/structured-data/article",
    "Product":       "https://developers.google.com/search/docs/appearance/structured-data/product",
    "FAQPage":       "https://developers.google.com/search/docs/appearance/structured-data/faqpage",
    "Organization":  "https://developers.google.com/search/docs/appearance/structured-data/organization",
    "LocalBusiness": "https://developers.google.com/search/docs/appearance/structured-data/local-business",
    "Event":         "https://developers.google.com/search/docs/appearance/structured-data/event",
    "Recipe":        "https://developers.google.com/search/docs/appearance/structured-data/recipe",
}


def load_google_docs() -> list[dict]:
    """Return a list of {schema_type, source, text} dicts."""
    docs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for schema_type, url in GOOGLE_DOCS.items():
            try:
                page.goto(url, timeout=20000)
                page.wait_for_timeout(2000)
                html = page.content()
                text = _parse_google_page(html, schema_type)
                if text:
                    docs.append({"schema_type": schema_type, "source": url, "text": text})
                    print(f"  [google-docs] {schema_type}: {len(text)} chars")
            except Exception as e:
                print(f"  [google-docs] WARN {schema_type}: {e}")
        browser.close()
    return docs


def _parse_google_page(html: str, schema_type: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    lines = [f"Google Rich Results: {schema_type}\n"]

    # Remove nav/header/footer noise
    for tag in soup(["nav", "header", "footer", "aside", "script", "style"]):
        tag.decompose()

    # Main article content
    article = soup.find("article") or soup.find("main") or soup.find("div", class_="devsite-article-body")
    target = article if article else soup.body

    if target:
        # Grab headings and paragraphs — captures required/recommended property tables
        for el in target.find_all(["h1", "h2", "h3", "p", "li", "td", "th"]):
            t = el.get_text(" ", strip=True)
            if t and len(t) > 10:
                lines.append(t)

    return "\n".join(lines)
