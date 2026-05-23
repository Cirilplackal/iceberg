from fastapi import APIRouter

from pydantic import BaseModel

from sse_starlette.sse import (
    EventSourceResponse
)

from app.rag.services.rag_service import (
    stream_rag_response
)

router = APIRouter()


class RAGRequest(BaseModel):
    message: str


@router.post("/rag")

async def rag_chat(
    request: RAGRequest
):

    async def event_generator():

        async for chunk in stream_rag_response(
            request.message
        ):

            yield {
                "data": chunk
            }

    return EventSourceResponse(
        event_generator()
    )