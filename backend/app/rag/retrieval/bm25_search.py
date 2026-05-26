from rank_bm25 import BM25Okapi

from qdrant_client.models import Filter, FieldCondition, MatchValue

from app.rag.vectorstore.qdrant_client import client

from app.rag.vectorstore.collections import COLLECTION_NAME


def bm25_search(query: str, filename: str = None, limit: int = 3):

    scroll_filter = None

    if filename:

        scroll_filter = Filter(
            must=[FieldCondition(key="filename", match=MatchValue(value=filename))]
        )

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=scroll_filter,
        limit=1000,
        with_payload=True,
        with_vectors=False,
    )

    if not points:

        return []

    documents = []

    payloads = []

    for point in points:

        text = point.payload["text"]

        documents.append(text.split())

        payloads.append(point.payload)

    bm25 = BM25Okapi(documents)

    tokenized_query = query.split()

    scores = bm25.get_scores(tokenized_query)

    ranked_results = sorted(zip(scores, payloads), key=lambda x: x[0], reverse=True)

    final_results = []

    for score, payload in ranked_results[:limit]:

        final_results.append({"score": round(float(score), 3), "payload": payload})

    return final_results
