from sentence_transformers import CrossEncoder

# LIGHTWEIGHT RERANKER MODEL

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank_results(query: str, results: list, top_k: int = 3):

    pairs = []

    for result in results:

        pairs.append([query, result["payload"]["text"]])

    scores = reranker.predict(pairs)

    reranked = []

    for result, score in zip(results, scores):

        result["rerank_score"] = round(float(score), 3)

        reranked.append(result)

    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)

    return reranked[:top_k]
