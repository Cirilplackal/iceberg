# Iceberg AI

Hybrid **Retrieval-Augmented Generation (RAG)** platform for grounded, citation-aware AI research.
Upload PDFs, build a semantic knowledge base, perform hybrid retrieval, rerank results, and generate context-grounded answers with transparent citations.

This is a full-stack project: the Python backend handles ingestion, retrieval, and Gemini grounding, while the Next.js frontend provides the upload and chat experience.

---

# Quick Start

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm
- A Google Gemini API key
- A Qdrant instance (cloud or local)

## 1) Start the backend

Open a terminal in the project root and run:

```powershell
# Go to the backend folder
cd backend

# Create a local Python environment
python -m venv .venv

# Activate it on Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r requirements.txt
```

Create a local environment file at `backend/.env`:

```env
# backend/.env
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=https://your-qdrant-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
```

Then start the API server:

```powershell
# Run the FastAPI app with hot reload enabled
uvicorn app.main:app --reload
```

The backend will be available at:

- API: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

## 2) Start the frontend

Open a second terminal and run:

```bash
# Move into the frontend app
cd frontend

# Install all frontend dependencies
npm install

# Start the Next.js development server
npm run dev
```

The frontend will be available at:

- Web app: `http://localhost:3000`

## 3) Use the app

1. Open the frontend in the browser.
2. Upload a PDF document.
3. Wait for ingestion and indexing to complete.
4. Ask a question about the uploaded document.
5. Review the generated answer and source citations.

> In practice, both services need to run at the same time: the frontend sends requests to the backend API, and the backend connects to Gemini and Qdrant.

---

# Features

- PDF ingestion & semantic indexing
- Hybrid retrieval (Semantic + BM25)
- Cross-encoder reranking
- Grounded Gemini responses
- Citation-aware responses
- Streaming AI responses (SSE)
- Metadata-aware retrieval filtering
- Smart chunking with overlap preservation
- Modular AI infrastructure architecture
- Qdrant Cloud vector database integration
- AI dashboard frontend

---

# System Architecture

```text
┌───────────────────────────────────────────────────────────────┐
│                       Frontend Layer                          │
│                 Next.js + React + Tailwind                   │
│                                                               │
│  · AI Dashboard                                               │
│  · PDF Upload UI                                              │
│  · Citation-aware Research Chat                               │
│  · Streaming Responses                                        │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────┐
│                       Backend API Layer                       │
│                      FastAPI + Python                         │
│                                                               │
│  /upload        → PDF ingestion                               │
│  /rag           → grounded response + citations               │
│  /rag/stream    → streaming grounded response                 │
│  /chat          → general Gemini streaming chat               │
└───────────────┬───────────────────────────────┬───────────────┘
                │                               │
                ▼                               ▼

     ┌────────────────────┐         ┌────────────────────┐
     │    Retrieval Core  │         │      Gemini LLM    │
     │                    │         │  gemini-2.5-flash  │
     └─────────┬──────────┘         └────────────────────┘
               │
               ▼

┌───────────────────────────────────────────────────────────────┐
│                    Hybrid RAG Pipeline                        │
└───────────────────────────────────────────────────────────────┘
               │
               ▼

      ┌─────────────────────────────┐
      │      Document Ingestion     │
      │                             │
      │ PDF → Extraction → Cleaning │
      │      → Chunking             │
      └──────────────┬──────────────┘
                     │
                     ▼

      ┌─────────────────────────────┐
      │      Embedding Layer        │
      │ SentenceTransformers        │
      │ all-MiniLM-L6-v2            │
      └──────────────┬──────────────┘
                     │
                     ▼

      ┌─────────────────────────────┐
      │        Vector Store         │
      │          Qdrant             │
      └──────────────┬──────────────┘
                     │
                     ▼

      ┌─────────────────────────────┐
      │      Retrieval Pipeline     │
      │                             │
      │  Semantic Retrieval         │
      │  +                          │
      │  BM25 Retrieval             │
      │  +                          │
      │  Hybrid Fusion              │
      │  +                          │
      │  Cross-Encoder Reranking    │
      └──────────────┬──────────────┘
                     │
                     ▼

      ┌─────────────────────────────┐
      │      Context Builder        │
      │  Prompt + Citations         │
      └──────────────┬──────────────┘
                     │
                     ▼

      ┌─────────────────────────────┐
      │      Grounded Response      │
      └─────────────────────────────┘
```

---

# Technology Stack


| Layer              | Technology                              |
| ------------------ | --------------------------------------- |
| Frontend           | Next.js 16                              |
| UI                 | React 19                                |
| Styling            | Tailwind CSS v4                         |
| Components         | shadcn/ui                               |
| Backend API        | FastAPI                                 |
| Streaming          | sse-starlette                           |
| LLM                | Google Gemini 2.5 Flash                 |
| Embeddings         | SentenceTransformers                    |
| Embedding Model    | `all-MiniLM-L6-v2`                      |
| Vector Database    | Qdrant                                  |
| PDF Parsing        | PyMuPDF                                 |
| Document Loading   | LangChain                               |
| Semantic Retrieval | Cosine similarity search                |
| Lexical Retrieval  | rank-bm25                               |
| Reranking          | CrossEncoder (`ms-marco-MiniLM-L-6-v2`) |
| Runtime            | Python 3.10+                            |


---

# Retrieval Architecture

Iceberg uses a **multi-stage retrieval pipeline**.

```text
User Query
     │
     ▼

┌─────────────────────┐
│ Query Embedding     │
└─────────┬───────────┘
          │
          ▼

 ┌───────────────────┐
 │ Semantic Search   │
 │ (Qdrant)          │
 └─────────┬─────────┘
           │

 ┌───────────────────┐
 │ BM25 Search       │
 │ (Keyword Search)  │
 └─────────┬─────────┘
           │

           ▼
   Hybrid Result Fusion
           │
           ▼

 ┌───────────────────┐
 │ Cross Encoder     │
 │ Reranker          │
 └─────────┬─────────┘
           │
           ▼

     Best Chunks
           │
           ▼

   Gemini Grounding
           │
           ▼

     Final Answer
```

---

# RAG Pipeline

## 1. Document Upload

PDFs are uploaded through `/upload`.

Pipeline:

```text
PDF
 ↓
Text Extraction
 ↓
Cleaning
 ↓
Smart Chunking
 ↓
Embedding Generation
 ↓
Qdrant Storage
```

---

## 2. Smart Chunking

Iceberg uses:

- overlap preservation
- paragraph-aware chunking
- semantic continuity preservation

Default:


| Setting    | Value |
| ---------- | ----- |
| Chunk Size | 800   |
| Overlap    | 150   |


---

## 3. Embedding Generation

Each chunk is embedded using:

```text
all-MiniLM-L6-v2
```

Output:

```text
384-dimensional vectors
```

---

## 4. Hybrid Retrieval

Iceberg performs:

### Semantic Retrieval

Meaning-based vector similarity search.

### BM25 Retrieval

Exact keyword-based lexical retrieval.

### Hybrid Fusion

Results are merged and deduplicated.

---

## 5. Reranking

Candidate chunks are reranked using:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

This improves:

- relevance precision
- grounding quality
- citation quality

---

## 6. Grounded Generation

Final chunks are injected into a Gemini prompt.

The LLM generates:

- grounded answers
- source-aware responses
- citation-backed outputs

---

# Backend Setup

## 1. Create a virtual environment

```powershell
# Move into the backend folder
cd backend

# Create a local environment for Python packages
python -m venv .venv

# Activate it on Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

---

## 2. Install Python dependencies

```powershell
# Install the API and retrieval dependencies
pip install -r requirements.txt
```

---

## 3. Configure environment variables

Create the file `backend/.env` with the values below:

```env
# backend/.env
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=https://your-qdrant-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
```

If you are running Qdrant locally instead of in the cloud, replace `QDRANT_URL` with your local URL such as `http://localhost:6333`.

---

## 4. Start the backend

```powershell
# Start the FastAPI backend with auto-reload enabled
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Swagger docs are available at:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

## 1. Install frontend dependencies

```bash
# Go to the frontend app
cd frontend

# Install Next.js and UI dependencies
npm install
```

---

## 2. Start the frontend

```bash
# Run the frontend in development mode
npm run dev
```

The frontend will be available at:

```text
http://localhost:3000
```

---

# API Overview


| Endpoint      | Method | Purpose                       |
| ------------- | ------ | ----------------------------- |
| `/upload`     | POST   | Upload & ingest PDFs          |
| `/rag`        | POST   | Grounded response + citations |
| `/rag/stream` | POST   | Streaming grounded response   |
| `/chat`       | POST   | General Gemini streaming chat |


---

# Current Project Structure

```text
iceberg/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── routes/
│   │   │    ├── upload.py
│   │   │    ├── rag.py
│   │   │    ├── rag_stream.py
│   │   │    └── chat.py
│   │   │
│   │   ├── rag/
│   │   │    │
│   │   │    ├── chunking/
│   │   │    ├── embeddings/
│   │   │    ├── retrieval/
│   │   │    ├── services/
│   │   │    └── vectorstore/
│   │   │
│   │   ├── ingestion/
│   │   └── llm/
│   │
│   ├── uploads/
│   │
│   ├── test_qdrant.py
│   ├── test_search.py
│   ├── test_bm25.py
│   ├── test_hybrid.py
│   └── test_reranker.py
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── types/
│   │
│   └── app/
│
└── README.md
```

---

# Engineering Challenges Solved


| Problem                    | Resolution                        |
| -------------------------- | --------------------------------- |
| BM25 noisy retrieval       | Metadata-aware filtering          |
| Giant document chunks      | Smart chunking pipeline           |
| Retrieval contamination    | Filename-scoped retrieval         |
| PDF layout noise           | Cleaning + structured ingestion   |
| Poor retrieval precision   | Hybrid retrieval + reranking      |
| Streaming architecture     | SSE async pipeline                |


---

# Current Capabilities

Iceberg currently supports:

- Hybrid Retrieval
- Semantic Search
- BM25 Keyword Search
- Cross-Encoder Reranking
- Citation-aware Responses
- Streaming AI Responses
- Metadata Filtering
- Smart Chunking
- Qdrant Cloud Integration
- Modular RAG Architecture

---

# Roadmap

Upcoming architecture evolution:

- Conversation memory
- Session-aware retrieval
- Multi-document workspaces
- Async ingestion pipelines
- Evaluation & observability
- LangGraph agent workflows
- Local model support (Ollama)
- Multi-model routing
- Retrieval tracing
- Production monitoring

---

