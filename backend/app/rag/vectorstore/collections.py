from qdrant_client.models import (
    VectorParams,
    Distance
)

from app.rag.vectorstore.qdrant_client import (
    client
)


COLLECTION_NAME = "iceberg_documents"


def create_collection():

    client.recreate_collection(
        collection_name=COLLECTION_NAME,

        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )