import json


def build_diff(before: list[dict], after: dict) -> dict:
    """Return a structured before/after diff for the frontend diff view."""
    before_str = json.dumps(before[0] if len(before) == 1 else before, indent=2)
    after_str = json.dumps(after, indent=2)
    return {
        "before": before_str,
        "after": after_str,
        "had_existing": len(before) > 0,
    }
