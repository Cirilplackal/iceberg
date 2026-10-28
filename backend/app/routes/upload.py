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
    # Save the uploaded PDF locally before processing it.
    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Extract text from the PDF so it can be split into searchable chunks.
    extracted_text = extract_text_from_pdf(file_path)

    # Use smart chunking to preserve context while keeping chunks digestible for retrieval.
    # The older chunk_text() alternative is kept as a reference in comments.
    chunks = smart_chunk_text(extracted_text)

    # Convert each chunk into a vector representation for semantic retrieval.
    embeddings = generate_embeddings(chunks)

    # Ensure the Qdrant collection exists before inserting new vectors.
    create_collection()

    # Store the chunks and their embeddings, with the source filename attached as metadata.
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
