from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.upload import router as upload_router

app = FastAPI(
    title="Iceberg AI"
)

app.include_router(chat_router)
app.include_router(upload_router)