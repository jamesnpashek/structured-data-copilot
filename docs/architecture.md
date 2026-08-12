# Architecture

## Overview

URL → Crawl → Extract → Normalize → Retrieve → Generate → Validate/Repair → Output

## Components

### Ingest
- **crawler.py** — fetches rendered HTML (httpx + Playwright fallback)
- **extractor.py** — strips noise, pulls existing JSON-LD blocks
- **normalizer.py** — detects schema types, cleans page text

### Corpus & Retrieval
- **schema_loader.py** — loads schema.org vocabulary docs
- **google_docs_loader.py** — loads Google rich results eligibility docs
- **chunker.py** — type-aware chunking for embedding
- **vector_store.py** — Chroma wrapper for upsert/query
- **retriever.py** — type-scoped retrieval (only fetches docs for detected types)

### Generate
- **generator.py** — RAG generation: page + retrieved docs → JSON-LD draft
- **repair_loop.py** — validate → fix loop (max 3 iterations)
- **prompts.py** — system message + user templates

### Validate
- **google_rules.py** — required/recommended property checks per schema type
- **schema_org.py** — @context, @type conformance

### Output
- **diff_builder.py** — before/after diff for the frontend
- **rationale.py** — plain-language summary for engineering handoff
