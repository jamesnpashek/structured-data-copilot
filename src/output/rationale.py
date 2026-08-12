def build_rationale(page: dict, jsonld: dict, validation: dict) -> str:
    schema_type = jsonld.get("@type", "Unknown")
    errors = validation.get("errors", [])
    warnings = validation.get("warnings", [])

    lines = [
        f"Generated {schema_type} structured data for this page.",
        f"Validation: {'passed' if validation['valid'] else f'{len(errors)} error(s) remaining'}.",
    ]
    if warnings:
        lines.append(f"Recommendations: {'; '.join(warnings[:3])}.")

    return " ".join(lines)
