"""
Validated few-shot JSON-LD examples embedded into the corpus.
These ground the LLM on what good, complete structured data looks like.
"""

import json

EXAMPLES: list[dict] = [
    {
        "schema_type": "Article",
        "source": "examples_library",
        "jsonld": {
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": "How AI Is Transforming Search Results",
            "author": {"@type": "Person", "name": "Jane Smith", "url": "https://example.com/authors/jane"},
            "datePublished": "2024-03-01T08:00:00+00:00",
            "dateModified": "2024-03-05T12:00:00+00:00",
            "image": {"@type": "ImageObject", "url": "https://example.com/article.jpg", "width": 1200, "height": 628},
            "publisher": {"@type": "Organization", "name": "Example News", "logo": {"@type": "ImageObject", "url": "https://example.com/logo.png"}},
            "description": "A look at how large language models are changing how search engines surface content.",
            "mainEntityOfPage": {"@type": "WebPage", "@id": "https://example.com/ai-search"},
        },
    },
    {
        "schema_type": "Product",
        "source": "examples_library",
        "jsonld": {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": "Wireless Noise-Cancelling Headphones",
            "image": "https://example.com/headphones.jpg",
            "description": "Premium over-ear headphones with 30-hour battery and active noise cancellation.",
            "brand": {"@type": "Brand", "name": "AudioPro"},
            "sku": "AH-2024-BLK",
            "offers": {
                "@type": "Offer",
                "url": "https://example.com/headphones",
                "priceCurrency": "USD",
                "price": "249.99",
                "availability": "https://schema.org/InStock",
                "priceValidUntil": "2025-01-01",
            },
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.7", "reviewCount": "1284"},
        },
    },
    {
        "schema_type": "FAQPage",
        "source": "examples_library",
        "jsonld": {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "What is structured data?",
                    "acceptedAnswer": {"@type": "Answer", "text": "Structured data is a standardized format for providing information about a page and classifying the page content. It helps search engines understand the content of a page."},
                },
                {
                    "@type": "Question",
                    "name": "How does JSON-LD work?",
                    "acceptedAnswer": {"@type": "Answer", "text": "JSON-LD is a method of encoding Linked Data using JSON. It is embedded in a <script> tag in the page's <head> section and is the format recommended by Google for structured data."},
                },
            ],
        },
    },
    {
        "schema_type": "Organization",
        "source": "examples_library",
        "jsonld": {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Acme Corporation",
            "url": "https://acme.example.com",
            "logo": "https://acme.example.com/logo.png",
            "sameAs": [
                "https://www.linkedin.com/company/acme",
                "https://twitter.com/acmecorp",
            ],
            "contactPoint": {"@type": "ContactPoint", "telephone": "+1-800-555-1234", "contactType": "customer service"},
        },
    },
    {
        "schema_type": "Event",
        "source": "examples_library",
        "jsonld": {
            "@context": "https://schema.org",
            "@type": "Event",
            "name": "Annual Data Science Summit",
            "startDate": "2025-09-15T09:00:00",
            "endDate": "2025-09-17T18:00:00",
            "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "location": {"@type": "Place", "name": "Minneapolis Convention Center", "address": {"@type": "PostalAddress", "streetAddress": "1301 2nd Ave S", "addressLocality": "Minneapolis", "addressRegion": "MN", "postalCode": "55403"}},
            "organizer": {"@type": "Organization", "name": "DataConf Inc.", "url": "https://dataconf.example.com"},
            "offers": {"@type": "Offer", "url": "https://dataconf.example.com/tickets", "price": "499", "priceCurrency": "USD", "availability": "https://schema.org/InStock"},
        },
    },
]


def load_examples() -> list[dict]:
    """Return examples formatted as text docs for embedding."""
    docs = []
    for ex in EXAMPLES:
        text = (
            f"Validated JSON-LD example for {ex['schema_type']}:\n\n"
            + json.dumps(ex["jsonld"], indent=2)
        )
        docs.append({"schema_type": ex["schema_type"], "source": ex["source"], "text": text})
        print(f"  [examples] {ex['schema_type']}: loaded")
    return docs
