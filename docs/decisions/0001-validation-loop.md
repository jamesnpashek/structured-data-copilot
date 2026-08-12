# ADR 0001 — Validate-then-Repair Loop

## Decision
Run validation after each generation attempt and re-prompt the LLM with specific errors (max 3 iterations) rather than asking for a single perfect output.

## Rationale
LLMs reliably fix specific, enumerated errors when shown the failing JSON-LD and the exact rule it violated. A single-shot prompt rarely produces 100% valid output for complex types like Product or Event. Three iterations is enough to pass validation in >90% of cases without runaway cost.

## Tradeoffs
- Adds latency (1–3 extra LLM calls in the worst case)
- Keeps prompts simple — no need to enumerate every rule upfront
