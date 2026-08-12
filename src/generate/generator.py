import json
from config import get_azure_client, AZURE_OPENAI_DEPLOYMENT
from generate.prompts import SYSTEM_MSG, USER_TEMPLATE


def generate(page: dict, context_docs: list[str]) -> dict:
    """Call the LLM to produce a JSON-LD draft from page content + retrieved docs."""
    client = get_azure_client()

    user_msg = USER_TEMPLATE.format(
        url=page.get("url", ""),
        schema_types=", ".join(page["schema_types"]),
        page_text=page["text"][:6000],
        context_docs="\n\n".join(context_docs)[:4000],
        existing_jsonld=json.dumps(page.get("existing_jsonld", []), indent=2),
    )

    resp = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": user_msg},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    return json.loads(resp.choices[0].message.content)
