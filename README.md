# Iceberg AI

Hybrid **retrieval-augmented generation (RAG)** platform for grounded, citation-aware research. Upload PDFs, query a vector knowledge base, and get answers backed by transparent source citations and similarity scores.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (Next.js)          http://localhost:3000          │
│  · PDF upload UI                                            │
│  · Citation-aware research chat                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend (FastAPI)           http://localhost:8000          │
│  · /upload   — ingest PDFs                                  │
│  · /rag      — grounded Q&A + sources (JSON)              │
│  · /rag/stream — streaming answers (SSE)                    │
│  · /chat     — general Gemini chat (SSE)                    │
└──────────┬─────────────────────────────┬────────────────────┘
           │                             │
           ▼                             ▼
    ┌──────────────┐              ┌──────────────┐
    │   Qdrant     │              │ Gemini 2.5   │
    │ vector store │              │   Flash      │
    └──────────────┘              └──────────────┘
```

| Layer        | Stack                                      |
|--------------|--------------------------------------------|
| Frontend     | Next.js 16, React 19, Tailwind 4, shadcn |
| Backend      | FastAPI, Python 3.10+                      |
| Embeddings   | `all-MiniLM-L6-v2` (384-dim)               |
| Vector DB    | Qdrant                                     |
| LLM          | Google Gemini (`gemini-2.5-flash`)         |
| PDF parsing  | PyMuPDF                                    |

## Quick start

### 1. Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `backend/.env`:

```env
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
```

```powershell
uvicorn app.main:app --reload
```

API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## RAG pipeline

1. **Upload** — PDF text is extracted, split into chunks (1000 chars, 200 overlap), and embedded.
2. **Store** — Vectors and metadata (`text`, `filename`, `chunk_index`) are upserted into Qdrant collection `iceberg_documents`.
3. **Query** — User question is embedded; top-3 chunks are retrieved (optional filename filter, score threshold ≥ 0.7).
4. **Generate** — Retrieved context is passed to Gemini for a grounded answer.
5. **Cite** — Frontend renders answer + ranked source cards (filename, score, preview).

## Project structure

```
iceberg/
├── backend/          # FastAPI API, RAG pipeline, Qdrant ingestion
│   ├── app/
│   │   ├── routes/   # chat, upload, rag, rag_stream
│   │   ├── rag/      # chunking, embeddings, retrieval, services
│   │   ├── llm/      # Gemini client
│   │   └── ingestion/
│   └── README.md
├── frontend/         # Next.js dashboard
│   ├── src/
│   │   ├── components/   # ChatPanel, UploadPanel, SourceCard
│   │   ├── services/     # askIceberg()
│   │   └── types/
│   └── README.md
└── README.md
```

## API overview

| Endpoint           | Method | Description                          |
|--------------------|--------|--------------------------------------|
| `/upload`          | POST   | Ingest PDF into Qdrant               |
| `/rag`             | POST   | Grounded answer + `sources` (JSON)   |
| `/rag/stream`      | POST   | Stream answer tokens (SSE, no sources) |
| `/chat`            | POST   | General Gemini chat (SSE)            |

The dashboard uses **`/rag`** for citation-aware research. Streaming endpoints are available for future UX.

## Documentation

- [Backend setup & API](backend/README.md)
- [Frontend setup & UI](frontend/README.md)

## Environment variables

| Variable         | Where    | Required | Description           |
|------------------|----------|----------|-----------------------|
| `GEMINI_API_KEY` | backend  | Yes      | Google Gemini API key |
| `QDRANT_URL`     | backend  | Yes      | Qdrant cluster URL    |
| `QDRANT_API_KEY` | backend  | Yes*     | Qdrant API key        |

\* Required for Qdrant Cloud.

Do not commit `.env` files.

## License

Private project — add a license if open-sourcing.
