import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, "ui"))

from ui.schemas.request import ChatRequest
from ui.schemas.response import ChatResponse

from ui.services.agent_service import AgentService

import json

router = APIRouter()


@router.post("/chat")

async def chat(request: ChatRequest):
    async def event_generator():
        async for event in AgentService.stream_chat(
            request.message,
            request.thread_id

        ):

            yield (
                "data: "
                + json.dumps(
                    event,
                    ensure_ascii=False
                )
                + "\n\n"
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"

    )