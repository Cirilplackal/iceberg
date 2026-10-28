from app.rag.retrieval.hybrid_search import hybrid_search

query = "rare earth elements"

results = hybrid_search(
    query=query, filename="rare-earth-elements-briefing-note-final-new-format (1).pdf"
)

for result in results:

    print("\n" + "=" * 50)

    print("Source:")
    print(result["source"])

    print("\nScore:")
    print(result["score"])

    print("\nChunk:")
    print(result["payload"]["text"][:800])
