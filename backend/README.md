# Iceberg Backend

FastAPI service that exposes a chat endpoint powered by Google Gemini.

## Prerequisites

- Python 3.10+
- A [Gemini API key](https://aistudio.google.com/apikey)

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

3. Create a `.env` file in `backend/`:

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

   Do not commit `.env` (it is listed in `.gitignore`).

## Run

From the `backend/` directory (with the venv activated):

```powershell
uvicorn app.main:app --reload
```

The API listens at `http://127.0.0.1:8000`.

Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API

### `POST /chat`

Send a message and receive a Gemini-generated reply.

**Request**

```json
{
  "message": "Hello!"
}
```

**Response**

```json
{
  "response": "..."
}
```

**Example (PowerShell)**

```powershell
curl.exe -X POST http://127.0.0.1:8000/chat `
  -H "Content-Type: application/json" `
  -d "{\"message\": \"Hello!\"}"
```

## Project layout

```
backend/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── routes/
│   │   └── chat.py      # /chat endpoint
│   └── llm/
│       └── gemini.py    # Gemini client and generate_response()
├── requirements.txt
└── .env                 # local only (not in git)
```

## Configuration

| Variable         | Required | Description              |
|------------------|----------|--------------------------|
| `GEMINI_API_KEY` | Yes      | Google Gemini API key    |

The model is configured in `app/llm/gemini.py` (currently `gemini-3.5-flash`).

## Dependencies

- **fastapi** — HTTP API
- **uvicorn** — ASGI server
- **google-generativeai** — Gemini SDK
- **python-dotenv** — load `.env`

> `google-generativeai` is deprecated; Google recommends migrating to `google-genai` later.
