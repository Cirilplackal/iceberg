# Iceberg Frontend

Next.js dashboard for **Iceberg AI** — a citation-aware, retrieval-augmented research assistant. Upload PDFs, ask questions, and view grounded answers with source citations and similarity scores.

## Prerequisites

- Node.js 18+
- [Iceberg backend](../backend) running at `http://localhost:8000`

## Setup

1. Install dependencies:

   ```bash
   cd frontend
   npm install
   ```

2. Start the dev server:

   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000)

Ensure the backend is running (`uvicorn app.main:app --reload` from `backend/`) before uploading or chatting.

## Scripts

| Command        | Description              |
|----------------|--------------------------|
| `npm run dev`  | Start dev server (port 3000) |
| `npm run build`| Production build         |
| `npm run start`| Run production server  |
| `npm run lint` | Run ESLint               |

## Features

- **Document ingestion** — PDF upload with drag-and-drop; displays chunk count, character count, and embedding dimensions after ingest
- **Grounded chat** — Questions answered via `POST /rag` with full answer + ranked sources
- **Citation UI** — Source cards show filename, chunk index, similarity score, relevance bar, and text preview
- **RAG pipeline feedback** — Loading state with retrieve → context → generate steps
- **Responsive layout** — Compact sidebar + full-width research panel; source grid on large screens

## Backend integration

The frontend talks to the FastAPI backend at `http://localhost:8000` (hardcoded in service/components for local dev).

| Endpoint        | Used by        | Purpose                          |
|-----------------|----------------|----------------------------------|
| `POST /upload`  | `UploadPanel`  | Ingest PDF into Qdrant           |
| `POST /rag`     | `askIceberg()` | Grounded Q&A with `sources` JSON |

Streaming (`POST /rag/stream`) is available on the backend but not used by the UI yet; the chat prioritizes citation transparency over token streaming.

### RAG response shape

```ts
{
  answer: string;
  sources: {
    filename: string;
    chunk_index: number;
    score: number;
    preview: string;
  }[];
}
```

## Project structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx      # Root layout, Poppins font
│   │   ├── page.tsx        # Main dashboard shell
│   │   └── globals.css     # Theme, AI surface utilities
│   ├── components/
│   │   ├── ChatPanel.tsx   # Research chat + citations
│   │   ├── UploadPanel.tsx # PDF upload + ingest stats
│   │   ├── SourceCard.tsx  # Citation card
│   │   ├── PanelHeader.tsx
│   │   ├── PipelineSteps.tsx
│   │   ├── StatusIndicator.tsx
│   │   └── ui/             # shadcn components
│   ├── services/
│   │   └── rag.ts          # askIceberg() → POST /rag
│   ├── types/
│   │   └── rag.ts          # Source, RAGResponse
│   └── lib/
│       └── utils.ts
├── package.json
└── README.md
```

## Tech stack

- **Next.js 16** (App Router)
- **React 19**
- **TypeScript**
- **Tailwind CSS 4**
- **shadcn/ui** + **Radix UI**
- **lucide-react** icons
- **Poppins** via `next/font/google`

## Configuration

To point at a different API host, update the fetch URLs in:

- `src/services/rag.ts`
- `src/components/UploadPanel.tsx`

A shared `NEXT_PUBLIC_API_URL` env variable can be added later for staging/production.

## Design

- Dark minimal UI with subtle violet/white ambient glows

