from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.upload import router as upload_router
from app.routes.rag import router as rag_router
from app.routes.rag_stream import router as rag_stream_router
from fastapi.middleware.cors import CORSMiddleware

# The app entry point for the FastAPI backend.
# This is where all API routers are registered and cross-origin requests are allowed.
app = FastAPI(title="Iceberg AI")

# Allow the frontend running on localhost:3000 to call the API during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register feature modules: chat, PDF upload, RAG generation, and streaming responses.
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(rag_router)
app.include_router(rag_stream_router)
