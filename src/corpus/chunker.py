"""
Type-aware text chunker. Splits long documents into overlapping chunks
while preserving schema_type and source metadata on every chunk.
"""

CHUNK_SIZE = 700    # characters per chunk
OVERLAP    = 100    # overlap between consecutive chunks


def chunk(doc: dict, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[dict]:
    """Split a single doc dict into overlapping chunks."""
    text  = doc["text"]
    meta  = {k: v for k, v in doc.items() if k != "text"}
    chunks: list[dict] = []

    start = 0
    while start < len(text):
        end        = min(start + chunk_size, len(text))
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append({"text": chunk_text, **meta})
        if end == len(text):
            break
        start += chunk_size - overlap

    return chunks


def chunk_all(docs: list[dict], **kwargs) -> list[dict]:
    """Chunk every doc in a list."""
    result = []
    for doc in docs:
        result.extend(chunk(doc, **kwargs))
    return result
