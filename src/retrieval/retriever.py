from retrieval.embedder import embed
from retrieval.vector_store import query

COLLECTION = "schema_corpus"


def retrieve(schema_types: list[str], n_per_type: int = 3) -> list[str]:
    """Retrieve relevant schema.org + Google docs for each detected schema type."""
    docs = []
    for schema_type in schema_types:
        query_text = f"schema.org {schema_type} required recommended properties JSON-LD"
        embedding = embed([query_text])[0]
        where = {"schema_type": {"$eq": schema_type}}
        results = query(COLLECTION, embedding, n_results=n_per_type, where=where)
        docs.extend(results)
    return docs
