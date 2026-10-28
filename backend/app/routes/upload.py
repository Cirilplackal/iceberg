"""Upload and indexing endpoints for PDF-based document ingestion.

This module accepts uploaded PDFs, extracts text, splits the content into chunks,
embeds those chunks, and stores the vector representations in Qdrant.
"""

import os
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.config import settings
from app.rag.embeddings.embedder import generate_embeddings


from app.rag.vectorstore.collections import (
    create_collection
)

from app.rag.vectorstore.ingestion import (
    store_embeddings
)

# from app.rag.chunking.splitter import (
#     chunk_text
# )

from app.rag.chunking.smart_chunker import smart_chunk_text

from app.ingestion.pdf_parser import extract_text_from_pdf

router = APIRouter()

UPLOAD_DIR = "uploads"
MAX_UPLOAD_BYTES = settings.max_upload_size_mb * 1024 * 1024


def validate_upload(file: UploadFile):
    """Ensure the uploaded file matches the app's supported file policy."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file is missing a filename.")

    suffix = Path(file.filename).suffix.lower()
    allowed_exts = settings.allowed_upload_extensions
    if suffix not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {suffix}. Allowed types: {', '.join(allowed_exts)}",
        )

    # Use a file pointer check so empty files are rejected before ingestion begins.
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size <= 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if file_size > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds the maximum upload size of {settings.max_upload_size_mb} MB.",
        )


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):
    """Persist a PDF, convert it into chunks, and store embeddings in Qdrant.

    The uploaded file is saved locally, text is extracted from the PDF, smart
    chunking is applied, embeddings are generated, and the vector data is stored
    so it can be retrieved in future RAG queries.
    """
    validate_upload(file)

    safe_filename = Path(file.filename).name
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    try:
        # Save the uploaded PDF locally before processing it.
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Extract text from the PDF so it can be split into searchable chunks.
        extracted_text = extract_text_from_pdf(file_path)

        # Use smart chunking to preserve context while keeping chunks digestible for retrieval.
        chunks = smart_chunk_text(extracted_text)

        # Convert each chunk into a vector representation for semantic retrieval.
        embeddings = generate_embeddings(chunks)

        # Ensure the Qdrant collection exists before inserting new vectors.
        create_collection()

        # Store the chunks and their embeddings, with the source filename attached as metadata.
        store_embeddings(
            chunks=chunks,
            embeddings=embeddings,
            filename=safe_filename,
        )

        return {
            "filename": safe_filename,
            "characters": len(extracted_text),
            "total_chunks": len(chunks),
            "embedding_dimension": len(embeddings[0]),
            "status": "stored in qdrant",
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"PDF upload failed: {str(exc)}") from exc
