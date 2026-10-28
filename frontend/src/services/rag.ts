import { RAGResponse } from "@/types/rag";

// Send the user question to the backend RAG endpoint and return the grounded answer.
export async function askIceberg(message: string): Promise<RAGResponse> {
  const response = await fetch(
    "http://localhost:8000/rag",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
      }),
    },
  );

  if (!response.ok) {
    throw new Error(`RAG request failed: ${response.status}`);
  }

  return response.json();
}
