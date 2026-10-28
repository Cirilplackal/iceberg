"""Application bootstrap for the Iceberg AI backend.

This module creates the FastAPI app and registers all API endpoints used by the
frontend, including chat, PDF upload, and retrieval-augmented generation routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.chat import router as chat_router
from app.routes.upload import router as upload_router
from app.routes.rag import router as rag_router
from app.routes.rag_stream import router as rag_stream_router

# The app entry point for the FastAPI backend.
# This is where all API routers are registered and cross-origin requests are allowed.
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Document-grounded AI search and retrieval application powered by Gemini and Qdrant.",
)

# Allow the frontend running on localhost:3000 to call the API during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Return basic service metadata for health checks and project discovery."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "ok",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """Provide a lightweight readiness endpoint for operational monitoring."""
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
    }


# Register feature modules: chat, PDF upload, RAG generation, and streaming responses.
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(rag_router)
app.include_router(rag_stream_router)
