import os

from app.rag.embeddings.embedder import (
    generate_embeddings
)

from app.rag.chunking.splitter import (
    chunk_text
)

from fastapi import APIRouter, UploadFile, File

from app.ingestion.pdf_parser import (
    extract_text_from_pdf
)

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/upload")

async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        content = await file.read()

        buffer.write(content)

    extracted_text = extract_text_from_pdf(
        file_path
    )
    
    chunks = chunk_text(extracted_text)
    embeddings = generate_embeddings(chunks)
    return {
        "filename": file.filename,
        "characters": len(extracted_text),
        "total_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]),
        "first_chunk": chunks[0],
    }