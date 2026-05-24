from qdrant_client.models import Filter, FieldCondition, MatchValue

from app.rag.embeddings.embedder import embedding_model

from app.rag.vectorstore.qdrant_client import client

from app.rag.vectorstore.collections import COLLECTION_NAME


SIMILARITY_THRESHOLD = 0.7


def search_documents(query: str, filename: str = None):

    query_embedding = embedding_model.encode(query)

    search_filter = None

    if filename:

        search_filter = Filter(
            must=[FieldCondition(key="filename", match=MatchValue(value=filename))]
        )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding.tolist(),
        query_filter=search_filter,
        limit=3,
    )

    filtered_results = [
        result for result in results.points if result.score >= SIMILARITY_THRESHOLD
    ]

    return filtered_results
