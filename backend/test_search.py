from app.rag.retrieval.search import (
    search_documents
)


query = "What is novarium?"


results = search_documents(query)


for result in results:

    print("\n")
    print("=" * 50)

    print("Score:")
    print(result.score)

    print("\nChunk:")
    print(result.payload["text"])