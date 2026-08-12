import json
from config import get_azure_client, AZURE_OPENAI_DEPLOYMENT
from validate.validator import validate
from generate.prompts import SYSTEM_MSG, REPAIR_TEMPLATE

MAX_ITERATIONS = 3


def repair_until_valid(draft: dict, page: dict) -> tuple[dict, dict]:
    """Validate → fix loop. Returns (final_jsonld, validation_report)."""
    client  = get_azure_client()
    current = draft

    for _ in range(MAX_ITERATIONS):
        report = validate(current)
        if report["valid"]:
            return current, report

        errors_text = "\n".join(f"- {e}" for e in report["errors"])
        user_msg = REPAIR_TEMPLATE.format(
            errors=errors_text,
            jsonld=json.dumps(current, indent=2),
            page_text=page["text"][:4000],
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
        current = json.loads(resp.choices[0].message.content)

    return current, validate(current)
