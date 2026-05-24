# Iceberg Backend

FastAPI service for Gemini chat (streaming), PDF ingestion, and retrieval-augmented generation (RAG) backed by Qdrant.

## Prerequisites

- Python 3.10+
- A [Gemini API key](https://aistudio.google.com/apikey)
- A [Qdrant](https://qdrant.tech/) instance (Qdrant Cloud or self-hosted)

## Setup

1. Create and activate a virtual environment:

   ```powershell
   cd backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

   The app also uses packages that may need to be installed separately if not already present:

   ```powershell
   pip install qdrant-client sentence-transformers sse-starlette pymupdf langchain-text-splitters
   ```

3. Create a `.env` file in `backend/`:

   ```env
   GEMINI_API_KEY=your_gemini_api_key
   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your_qdrant_api_key
   ```

   Do not commit `.env` (it is listed in `.gitignore`).

4. Ensure the `uploads/` directory exists (PDFs are saved there on upload).

## Run

From the `backend/` directory (with the venv activated):

```powershell
uvicorn app.main:app --reload
```

The API listens at `http://127.0.0.1:8000`.

Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API

### `POST /chat`

Stream a Gemini reply over Server-Sent Events (SSE).

**Request**

```json
{
  "message": "Hello!"
}
```

**Response**

SSE stream; each event has a `data` field containing a text chunk.

**Example (PowerShell)**

```powershell
curl.exe -N -X POST http://127.0.0.1:8000/chat `
  -H "Content-Type: application/json" `
  -d "{\"message\": \"Hello!\"}"
```

### `POST /upload`

Upload a PDF, extract text, chunk it, embed chunks, and store vectors in Qdrant.

**Request**

`multipart/form-data` with a `file` field (PDF).

**Response**

```json
{
  "filename": "document.pdf",
  "characters": 12345,
  "total_chunks": 42,
  "embedding_dimension": 384,
  "status": "stored in qdrant"
}
```

**Example (PowerShell)**

```powershell
curl.exe -X POST http://127.0.0.1:8000/upload `
  -F "file=@.\uploads\document.pdf"
```

On first upload, the `iceberg_documents` collection is created in Qdrant (384-dimensional cosine vectors, with a keyword index on `filename`).

### `POST /rag`

Ask a question grounded in uploaded documents. Returns a JSON answer with source citations.

**Request**

```json
{
  "message": "What are rare earth elements used for?",
  "filename": "optional-document.pdf"
}
```

`filename` is optional; when set, retrieval is limited to chunks from that file.

**Response**

```json
{
  "answer": "...",
  "sources": [
    {
      "filename": "document.pdf",
      "chunk_index": 0,
      "score": 0.82,
      "preview": "..."
    }
  ]
}
```

If no chunks meet the similarity threshold (0.7), `answer` reports that no relevant information was found and `sources` is empty.

**Example (PowerShell)**

```powershell
curl.exe -X POST http://127.0.0.1:8000/rag `
  -H "Content-Type: application/json" `
  -d "{\"message\": \"Summarize the briefing note.\"}"
```

### `POST /rag/stream`

Same retrieval and grounding as `/rag`, but streams the Gemini answer over SSE.

**Request**

```json
{
  "message": "What are rare earth elements used for?"
}
```

**Response**

SSE stream of answer chunks.

**Example (PowerShell)**

```powershell
curl.exe -N -X POST http://127.0.0.1:8000/rag/stream `
  -H "Content-Type: application/json" `
  -d "{\"message\": \"Summarize the briefing note.\"}"
```

## RAG pipeline

1. **Upload** — PDF text is extracted (`pymupdf`), split into chunks (`langchain-text-splitters`), and embedded with `all-MiniLM-L6-v2` (384 dimensions).
2. **Store** — Vectors and metadata (`text`, `filename`, `chunk_index`) are upserted into Qdrant collection `iceberg_documents`.
3. **Query** — The user question is embedded; top matches are filtered by score (≥ 0.7) and optionally by `filename`.
4. **Generate** — Retrieved chunks are passed to Gemini (`gemini-2.5-flash`) as context for a grounded answer.

## Utilities

| Script | Purpose |
|--------|---------|
| `reset_collection.py` | Delete the `iceberg_documents` Qdrant collection (use before re-ingesting after schema changes) |
| `test_models.py` | List available Gemini models |
| `test_qdrant.py` | Verify Qdrant connectivity |
| `test_search.py` | Exercise semantic search |

Run from `backend/` with the venv activated, e.g. `python reset_collection.py`.

## Project layout

```
backend/
├── app/
│   ├── main.py                 # FastAPI app and router registration
│   ├── routes/
│   │   ├── chat.py             # POST /chat (SSE)
│   │   ├── upload.py           # POST /upload
│   │   ├── rag.py              # POST /rag (JSON)
│   │   └── rag_stream.py       # POST /rag/stream (SSE)
│   ├── llm/
│   │   └── gemini.py           # Gemini client and streaming
│   ├── ingestion/
│   │   └── pdf_parser.py       # PDF text extraction
│   └── rag/
│       ├── chunking/splitter.py
│       ├── embeddings/embedder.py
│       ├── retrieval/search.py
│       ├── services/rag_service.py
│       └── vectorstore/        # Qdrant client, collection, ingestion
├── uploads/                    # Uploaded PDFs (local)
├── requirements.txt
└── .env                        # local only (not in git)
```

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `QDRANT_URL` | Yes | Qdrant cluster URL |
| `QDRANT_API_KEY` | Yes* | Qdrant API key (*required for Qdrant Cloud) |

The Gemini model is set in `app/llm/gemini.py` (currently `gemini-2.5-flash`). The embedding model is `all-MiniLM-L6-v2` in `app/rag/embeddings/embedder.py`.

## Dependencies

- **fastapi** — HTTP API
- **uvicorn** — ASGI server
- **google-generativeai** — Gemini SDK
- **python-dotenv** — load `.env`
- **qdrant-client** — vector store
- **sentence-transformers** — local embeddings (`all-MiniLM-L6-v2`)
- **sse-starlette** — SSE responses for `/chat` and `/rag/stream`
- **pymupdf** — PDF parsing
- **langchain-text-splitters** — text chunking

> `google-generativeai` is deprecated; Google recommends migrating to `google-genai` later.
