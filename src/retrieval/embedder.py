from config import get_azure_client, AZURE_OPENAI_EMB_DEPLOYMENT


def embed(texts: list[str]) -> list[list[float]]:
    client = get_azure_client()
    resp = client.embeddings.create(model=AZURE_OPENAI_EMB_DEPLOYMENT, input=texts)
    return [item.embedding for item in resp.data]
