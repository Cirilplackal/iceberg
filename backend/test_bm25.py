from app.rag.retrieval.bm25_search import bm25_search

query = "rare earth elements"

results = bm25_search(query=query, filename="rare-earth-elements-briefing-note-final-new-format (1).pdf")

for result in results:

    print("\n" + "=" * 50)

    print("Score:")
    print(result["score"])

    print("\nChunk:")
    print(result["payload"]["text"])
