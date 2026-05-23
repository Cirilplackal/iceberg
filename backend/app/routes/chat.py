from fastapi import APIRouter
from pydantic import BaseModel

from sse_starlette.sse import EventSourceResponse

from app.llm.gemini import stream_response

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat(request: ChatRequest):

    async def event_generator():

        async for chunk in stream_response(
            request.message
        ):
            yield {
                "data": chunk
            }

    return EventSourceResponse(
        event_generator()
    )