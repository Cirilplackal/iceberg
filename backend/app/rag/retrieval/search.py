from qdrant_client.models import Filter, FieldCondition, MatchValue

from app.config import settings
from app.rag.embeddings.embedder import embedding_model
from app.rag.vectorstore.qdrant_client import client
from app.rag.vectorstore.collections import COLLECTION_NAME


SIMILARITY_THRESHOLD = settings.similarity_threshold


def search_documents(query: str, filename: str = None, limit: int = 3):
    """Return relevant document chunks, optionally limited to a specific file."""
    query_embedding = embedding_model.encode(query)

    search_filter = None
    if filename:
        search_filter = Filter(
            must=[FieldCondition(key="filename", match=MatchValue(value=filename))]
        )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=search_filter,
        limit=min(limit, settings.max_retrieval_results),
    )

    filtered_results = [
        result for result in results.points if result.score >= SIMILARITY_THRESHOLD
    ]

    return filtered_results
