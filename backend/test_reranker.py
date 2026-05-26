from app.rag.retrieval.hybrid_search import hybrid_search

from app.rag.retrieval.reranker import rerank_results

query = "What are rare earth elements?"

results = hybrid_search(
    query=query, filename="rare-earth-elements-briefing-note-final-new-format (1).pdf"
)

reranked = rerank_results(query=query, results=results)

for result in reranked:

    print("\n" + "=" * 50)

    print("Source:")
    print(result["source"])

    print("\nRerank Score:")
    print(result["rerank_score"])

    print("\nChunk:")
    print(result["payload"]["text"][:800])
