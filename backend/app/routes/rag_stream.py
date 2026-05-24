from fastapi import APIRouter

from pydantic import BaseModel

from sse_starlette.sse import EventSourceResponse

from app.rag.services.rag_service import stream_rag_response

router = APIRouter()


class RAGStreamRequest(BaseModel):
    message: str


@router.post("/rag/stream")
async def rag_stream_chat(request: RAGStreamRequest):

    async def event_generator():

        async for chunk in stream_rag_response(request.message):

            yield {"data": chunk}

    return EventSourceResponse(event_generator())
