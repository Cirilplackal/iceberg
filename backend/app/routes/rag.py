from fastapi import APIRouter

from pydantic import BaseModel

from app.rag.services.rag_service import generate_rag_response

router = APIRouter()


class RAGRequest(BaseModel):
    message: str
    filename: str | None = None


@router.post("/rag")
async def rag_chat(request: RAGRequest):

    response = await generate_rag_response(
        query=request.message, filename=request.filename
    )

    return response
