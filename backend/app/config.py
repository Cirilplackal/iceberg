"""Application configuration and environment validation.

This module centralizes the settings used across the backend so the app can be
configured cleanly for local development and production deployments.
"""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@dataclass(frozen=True)
class Settings:
    app_name: str = "Iceberg AI"
    app_version: str = "0.1.0"
    gemini_api_key: str = field(default_factory=lambda: _get_required_env("GEMINI_API_KEY"))
    qdrant_url: str = field(default_factory=lambda: _get_required_env("QDRANT_URL"))
    qdrant_api_key: str | None = field(default_factory=lambda: os.getenv("QDRANT_API_KEY") or None)
    collection_name: str = field(default_factory=lambda: os.getenv("COLLECTION_NAME", "iceberg_documents"))
    similarity_threshold: float = field(default_factory=lambda: float(os.getenv("SIMILARITY_THRESHOLD", "0.5")))
    max_retrieval_results: int = field(default_factory=lambda: int(os.getenv("MAX_RETRIEVAL_RESULTS", "5")))
    max_upload_size_mb: int = field(default_factory=lambda: int(os.getenv("MAX_UPLOAD_SIZE_MB", "25")))
    allowed_upload_extensions: tuple[str, ...] = field(
        default_factory=lambda: tuple(
            ext.strip().lower()
            for ext in os.getenv("ALLOWED_UPLOAD_EXTENSIONS", ".pdf").split(",")
            if ext.strip()
        )
    )
    cors_origins: tuple[str, ...] = field(
        default_factory=lambda: tuple(
            origin.strip()
            for origin in os.getenv(
                "CORS_ORIGINS",
                "http://localhost:3000,http://127.0.0.1:3000",
            ).split(",")
            if origin.strip()
        )
    )


settings = Settings()
