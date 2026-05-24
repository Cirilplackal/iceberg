from qdrant_client.models import VectorParams, Distance, PayloadSchemaType

from app.rag.vectorstore.qdrant_client import client


COLLECTION_NAME = "iceberg_documents"


def create_collection():

    collections = client.get_collections()

    collection_names = [collection.name for collection in collections.collections]

    if COLLECTION_NAME not in collection_names:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

        # CREATE PAYLOAD INDEX

        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="filename",
            field_schema=PayloadSchemaType.KEYWORD,
        )
