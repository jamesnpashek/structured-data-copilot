from ingest.crawler import fetch_page
from ingest.extractor import extract
from ingest.normalizer import normalize
from retrieval.retriever import retrieve
from generate.generator import generate
from generate.repair_loop import repair_until_valid
from validate.validator import validate
from output.diff_builder import build_diff
from output.rationale import build_rationale


def run_pipeline(url: str) -> dict:
    raw_html = fetch_page(url)
    content, existing_jsonld = extract(raw_html)
    page = normalize(content, existing_jsonld)

    context_docs = retrieve(page["schema_types"])
    draft = generate(page, context_docs)
    final, validation_report = repair_until_valid(draft, page)

    diff = build_diff(existing_jsonld, final)
    rationale = build_rationale(page, final, validation_report)

    return {
        "url": url,
        "existing_jsonld": existing_jsonld,
        "generated_jsonld": final,
        "diff": diff,
        "validation": validation_report,
        "rationale": rationale,
    }
