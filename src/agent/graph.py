from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from agent.state import AgentState

from agent.nodes import (
    classifier_node,
    law_node,
    football_node,
    worldcup_node,
    worldcup2026_node,
    news_node,
    summarize_node,
    fallback_node,

    football_tool_node,
    worldcup_tool_node,
    worldcup2026_tool_node,
    news_tool_node
)

from tools.search_tools import search_latest_news

from agent.router import (
    route_classifier,

    route_football_tools,
    route_worldcup_tools,
    route_news_tools,

    route_after_football_tool,
    route_after_worldcup_tool,
    route_after_worldcup2026_tool,

    route_after_fallback_tool
)

# ==================================================
# GRAPH
# ==================================================

builder = StateGraph(AgentState)

# ==================================================
# NODES
# ==================================================

builder.add_node("classifier", classifier_node)

builder.add_node("law", law_node)

builder.add_node("football", football_node)
builder.add_node("football_tool", football_tool_node)

builder.add_node("worldcup", worldcup_node)
builder.add_node("worldcup_tool", worldcup_tool_node)

builder.add_node("worldcup2026", worldcup2026_node)
builder.add_node("worldcup2026_tool", worldcup2026_tool_node)

builder.add_node("news", news_node)
builder.add_node("news_tool", news_tool_node)

# fallback
builder.add_node("fallback_news", fallback_node)
builder.add_node("fallback_tool", ToolNode([search_latest_news]))
builder.add_node("summarize", summarize_node)

# ==================================================
# START
# ==================================================

builder.add_edge(
    START,
    "classifier"
)

# ==================================================
# CLASSIFIER
# ==================================================

builder.add_conditional_edges(
    "classifier",
    route_classifier,
    {
        "law": "law",
        "football_data": "football",
        "worldcup_data": "worldcup",
        "worldcup2026": "worldcup2026",
        "general_news": "news"
    }
)

# ==================================================
# LAW
# ==================================================

builder.add_edge(
    "law",
    "summarize"
)

# ==================================================
# FOOTBALL
# ==================================================

builder.add_conditional_edges(
    "football",
    route_football_tools,
    {
        "tool": "football_tool",
        "summarize": "summarize"
    }
)

builder.add_conditional_edges(
    "football_tool",
    route_after_football_tool,
    {
        "football": "football",
        "fallback_news": "fallback_news"
    }
)

# ==================================================
# WORLDCUP HISTORY
# ==================================================

builder.add_conditional_edges(
    "worldcup",
    route_worldcup_tools,
    {
        "tool": "worldcup_tool",
        "summarize": "summarize"
    }
)

builder.add_conditional_edges(
    "worldcup_tool",
    route_after_worldcup_tool,
    {
        "worldcup": "worldcup",
        "fallback_news": "fallback_news"
    }
)

# ==================================================
# WORLDCUP 2026
# ==================================================

builder.add_conditional_edges(
    "worldcup2026",
    route_worldcup_tools,
    {
        "tool": "worldcup2026_tool",
        "summarize": "summarize"
    }
)

builder.add_conditional_edges(
    "worldcup2026_tool",
    route_after_worldcup2026_tool,
    {
        "worldcup2026": "worldcup2026",
        "fallback_news": "fallback_news"
    }
)

# ==================================================
# NEWS
# ==================================================

builder.add_conditional_edges(
    "news",
    route_news_tools,
    {
        "tool": "news_tool",
        "summarize": "summarize"
    }
)

builder.add_edge(
    "news_tool",
    "news"
)

# ==================================================
# FALLBACK
# ==================================================

builder.add_edge("fallback_news","fallback_tool")

builder.add_conditional_edges(
    "fallback_tool",
    route_after_fallback_tool,
    {
        "summarize": "summarize"
    }
)

# ==================================================
# END
# ==================================================

builder.add_edge("summarize",END)

memory = MemorySaver()

graph = builder.compile(checkpointer=memory)
