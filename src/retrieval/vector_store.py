import chromadb
from config import CHROMA_PERSIST_DIR

_client = None


def get_client() -> chromadb.ClientAPI:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    return _client


def get_or_create_collection(name: str):
    return get_client().get_or_create_collection(name)


def upsert(collection_name: str, ids: list[str],
           embeddings: list[list[float]], documents: list[str],
           metadatas: list[dict] | None = None):
    col = get_or_create_collection(collection_name)
    col.upsert(ids=ids, embeddings=embeddings,
               documents=documents, metadatas=metadatas or [{}] * len(ids))


def query(collection_name: str, query_embedding: list[float],
          n_results: int = 5, where: dict | None = None) -> list[str]:
    col = get_or_create_collection(collection_name)
    kwargs = {"query_embeddings": [query_embedding], "n_results": n_results}
    if where:
        kwargs["where"] = where
    results = col.query(**kwargs)
    return results["documents"][0] if results["documents"] else []
