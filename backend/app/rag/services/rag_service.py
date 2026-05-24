from app.rag.retrieval.search import search_documents

from app.llm.gemini import model

from app.llm.gemini import stream_response


def build_rag_prompt(query: str, search_results):

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

    # STEP 1
    # Semantic Retrieval

    search_results = search_documents(query=query, filename=filename)

    if not search_results:
        return {"answer": ("No relevant information " "was found."), "sources": []}

    # STEP 2
    # Build RAG Prompt

    prompt = build_rag_prompt(query=query, search_results=search_results)

    # STEP 3
    # Gemini Generation

    response = model.generate_content(prompt)

    # STEP 4
    # Return Grounded Response
    # with Sources

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

    # STEP 1
    # Semantic Retrieval

    search_results = search_documents(query)

    if not search_results:

        yield "No relevant information was found in the knowledge base."

        return

    # STEP 2
    # Build Grounded Prompt

    prompt = build_rag_prompt(query=query, search_results=search_results)

    # STEP 3
    # Stream Gemini Response

    async for chunk in stream_response(prompt):

        yield chunk
