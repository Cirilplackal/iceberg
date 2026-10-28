from qdrant_client.models import (
    PointStruct
)

from app.rag.vectorstore.qdrant_client import (
    client
)

from app.rag.vectorstore.collections import (
    COLLECTION_NAME
)


def store_embeddings(
    chunks,
    embeddings,
    filename
):

    points = []

    for index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):

        points.append(
            PointStruct(
                id=index,

                vector=embedding.tolist(),

                payload={
                    "text": chunk,
                    "filename": filename,
                    "chunk_index": index
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )