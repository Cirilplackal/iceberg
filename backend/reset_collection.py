from app.rag.vectorstore.qdrant_client import client

from app.rag.vectorstore.collections import COLLECTION_NAME

client.delete_collection(collection_name=COLLECTION_NAME)

print("Collection deleted.")
