from app.rag.embeddings.embedder import (
    embedding_model
)

from app.rag.vectorstore.qdrant_client import (
    client
)

from app.rag.vectorstore.collections import (
    COLLECTION_NAME
)


def search_documents(query: str):

    query_embedding = embedding_model.encode(
        query
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,

        query=query_embedding.tolist(),

        limit=3
    )

    return results.points