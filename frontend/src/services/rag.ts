import { RAGResponse } from "@/types/rag";

/**
 * Sends a user question to the backend RAG endpoint and returns the grounded answer.
 *
 * This is the primary frontend call used when a user asks a document-based question.
 */
export async function askIceberg(message: string): Promise<RAGResponse> {
  const response = await fetch("http://localhost:8000/rag", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
    }),
  });

  if (!response.ok) {
    throw new Error(`RAG request failed: ${response.status}`);
  }

  return response.json();
}
