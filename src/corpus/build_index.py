"""
One-time script: load all corpus docs, chunk, embed, and upsert into Chroma.
Run from the repo root:  python src/corpus/build_index.py
"""

import sys
import os

# Make src/ importable when run directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from corpus.schema_loader import load_schema_docs
from corpus.google_docs_loader import load_google_docs
from corpus.examples_loader import load_examples
from corpus.chunker import chunk_all
from retrieval.embedder import embed
from retrieval.vector_store import upsert

COLLECTION  = "schema_corpus"
BATCH_SIZE  = 50


def build_index():
    print("=== Loading docs ===")
    docs: list[dict] = []

    print("schema.org property definitions...")
    docs.extend(load_schema_docs())

    print("Google rich results docs...")
    docs.extend(load_google_docs())

    print("Validated examples...")
    docs.extend(load_examples())

    print(f"\n=== Chunking {len(docs)} docs ===")
    chunks = chunk_all(docs)
    print(f"{len(chunks)} total chunks")

    print("\n=== Embedding + indexing ===")
    for i in range(0, len(chunks), BATCH_SIZE):
        batch      = chunks[i : i + BATCH_SIZE]
        texts      = [c["text"] for c in batch]
        embeddings = embed(texts)
        ids        = [f"chunk_{i + j}" for j in range(len(batch))]
        metadatas  = [
            {"schema_type": c.get("schema_type", ""), "source": c.get("source", "")}
            for c in batch
        ]
        upsert(COLLECTION, ids=ids, embeddings=embeddings,
               documents=texts, metadatas=metadatas)
        print(f"  indexed {min(i + BATCH_SIZE, len(chunks))}/{len(chunks)}")

    print("\n=== Done — corpus ready ===")


if __name__ == "__main__":
    build_index()
