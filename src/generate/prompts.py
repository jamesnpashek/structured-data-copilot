SYSTEM_MSG = """\
You are a structured data expert. Given page content and relevant schema.org \
documentation, generate valid JSON-LD that maximizes Google rich result eligibility. \
Return ONLY a valid JSON-LD object — no explanation, no markdown fences.\
"""

USER_TEMPLATE = """\
PAGE URL: {url}
SCHEMA TYPES TO GENERATE: {schema_types}

PAGE CONTENT:
{page_text}

RELEVANT SCHEMA.ORG DOCUMENTATION:
{context_docs}

EXISTING JSON-LD (if any — use as a base, improve it):
{existing_jsonld}

Generate complete, valid JSON-LD for the schema types listed. Include all \
required and recommended properties for Google rich results eligibility. \
Return only the JSON-LD object.\
"""

REPAIR_TEMPLATE = """\
The following JSON-LD failed validation with these errors:

ERRORS:
{errors}

JSON-LD TO FIX:
{jsonld}

PAGE CONTENT:
{page_text}

Fix only the failing properties. Return the corrected JSON-LD object only.\
"""
