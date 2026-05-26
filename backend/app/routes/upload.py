import os

from app.rag.embeddings.embedder import (
    generate_embeddings
)


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

    # chunks = chunk_text(extracted_text)

    chunks = smart_chunk_text(extracted_text)

    embeddings = generate_embeddings(chunks)

    # creating collection in qdrant
    create_collection()

    # storing embeddings in qdrant
    store_embeddings(
        chunks=chunks,
        embeddings=embeddings,
        filename=file.filename
    )

    return {
        "filename": file.filename,
        "characters": len(extracted_text),
        "total_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]),
        "status": "stored in qdrant"
    }
