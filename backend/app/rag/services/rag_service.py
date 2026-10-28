"""RAG orchestration for retrieving relevant passages and grounding answers.

This service connects vector search with Gemini generation so the model answers
questions using the most relevant document context instead of generic knowledge.
"""

from app.rag.retrieval.search import search_documents

from app.llm.gemini import model

from app.llm.gemini import stream_response


def build_rag_prompt(query: str, search_results):
    """Create a grounded prompt that includes retrieved document chunks as context."""
    # Combine the retrieved document chunks into one context block.
    # This lets the model answer using only the most relevant passages rather than guessing.
    context = "\n\n".join([result.payload["text"] for result in search_results])

    prompt = f"""
You are a helpful AI research assistant.

Answer the user's question using ONLY
the provided context.

If the answer is not available in the context,
say that the information was not found.

Context:
{context}

Question:
{query}
"""

    return prompt


async def generate_rag_response(query: str, filename: str = None):
    """Return a grounded answer and source references for a user query."""
    # Step 1: retrieve the most relevant document chunks from the vector store.
    search_results = search_documents(query=query, filename=filename)

    if not search_results:
        return {"answer": ("No relevant information " "was found."), "sources": []}

    # Step 2: turn retrieved chunks into a grounded prompt for Gemini.
    prompt = build_rag_prompt(query=query, search_results=search_results)

    # Step 3: ask Gemini to answer using only the retrieved context.
    response = model.generate_content(prompt)

    # Step 4: return the answer and source metadata for citation display in the UI.
    return {
        "answer": response.text,
        "sources": [
            {
                "filename": result.payload["filename"],
                "chunk_index": result.payload["chunk_index"],
                "score": round(result.score, 3),
                "preview": result.payload["text"][:300],
            }
            for result in search_results
        ],
    }


async def stream_rag_response(query: str):
    """Stream a grounded answer to the client as Gemini produces response chunks."""
    # Step 1: fetch relevant document chunks for the query.
    search_results = search_documents(query)

    if not search_results:
        yield "No relevant information was found in the knowledge base."
        return

    # Step 2: build a context-aware prompt before streaming the answer.
    prompt = build_rag_prompt(query=query, search_results=search_results)

    # Step 3: stream the Gemini output chunk by chunk to the frontend.
    async for chunk in stream_response(prompt):
        yield chunk
