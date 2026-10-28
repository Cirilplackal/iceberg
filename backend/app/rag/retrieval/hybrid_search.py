from app.rag.retrieval.search import search_documents

from app.rag.retrieval.bm25_search import bm25_search


def hybrid_search(query: str, filename: str = None, limit: int = 5):

    semantic_results = search_documents(query=query, filename=filename, limit=limit)

    bm25_results = bm25_search(query=query, filename=filename, limit=limit)

    combined_results = []

    seen_texts = set()

    # SEMANTIC RESULTS

    for result in semantic_results:

        text = result.payload["text"]

        if text not in seen_texts:

            combined_results.append(
                {
                    "source": "semantic",
                    "score": round(result.score, 3),
                    "payload": result.payload,
                }
            )

            seen_texts.add(text)

    # BM25 RESULTS

    for result in bm25_results:

        text = result["payload"]["text"]

        if text not in seen_texts:

            combined_results.append(
                {
                    "source": "bm25",
                    "score": result["score"],
                    "payload": result["payload"],
                }
            )

            seen_texts.add(text)

    return combined_results[:limit]
