# Structured Data Copilot

Paste a URL, get production-ready JSON-LD structured data back — validated against schema.org vocabulary and Google rich results requirements.

## How it works

1. **Crawl** — fetches and renders the target page
2. **Extract** — pulls existing JSON-LD and strips page content to plain text
3. **Retrieve** — fetches relevant schema.org + Google docs from a vector store (type-scoped)
4. **Generate** — prompts GPT-4o with page content + retrieved docs to produce a JSON-LD draft
5. **Validate → Repair** — checks required/recommended properties, re-prompts with specific errors (up to 3 iterations)
6. **Output** — returns a before/after diff and plain-language rationale

## Project structure

```
apps/web/          Next.js frontend (Vercel)
packages/schema-validator/   OSS validation rules package
src/               Python backend (FastAPI + RAG pipeline)
eval/              Evaluation harness and labeled test set
docs/              Architecture and decision records
```

## Quick start

```bash
cp .env.example .env
# add OPENAI_API_KEY

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

docker-compose up -d          # start local Chroma
bash scripts/build_corpus.sh  # one-time corpus build
bash scripts/run_local.sh     # start API on :8000
```
