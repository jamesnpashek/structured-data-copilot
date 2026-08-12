#!/bin/bash
set -e
cd "$(dirname "$0")/.."
source .venv/bin/activate
python src/corpus/schema_loader.py
python src/corpus/google_docs_loader.py
python src/corpus/examples_loader.py
python src/corpus/build_index.py
echo "Corpus built."
