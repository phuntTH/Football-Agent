from pydantic import BaseModel


class ToolTrace(BaseModel):
    tool: str
    args: dict


class ChatResponse(BaseModel):
    answer: str
    trace: list[ToolTrace]