from typing import Annotated, Literal

from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    route: Literal["law","chatbot","football_data","worldcup_data"]
    summary: str
    need_fallback: bool

