from langchain_core.messages import (AIMessage,HumanMessage,SystemMessage,ToolMessage)

import os   
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.llm import llm
from agent.prompts import (CLASSIFIER_PROMPT,LAW_PROMPT,FOOTBALL_PROMPT,WORLDCUP_PROMPT,NEWS_PROMPT,WORLDCUP_2026_PROMPT,FALLBACK_PROMPT)

from tools.law_tools import search_ifab_law

from tools.search_tools import search_latest_news

from tools.football_tools import (get_wc_matches,get_match_events,get_match_lineup,get_match_statistics)

from tools.worldcup_tools import (get_world_cup_overview)

from tools.worldcup2026_tools import (
    get_wc2026_info,
    get_wc2026_matches,
    get_wc2026_standings,
    get_wc2026_scorers,
    get_wc2026_match_detail,
    get_wc2026_team,
    get_wc2026_team_matches,
    get_wc2026_team_matches_by_date
)

from agent.router import keyword_router

from langchain_community.tools import TavilySearchResults

def get_tool_history(messages):
    cleaned = []

    for msg in messages:

        if isinstance(msg,(HumanMessage,ToolMessage,AIMessage)):
            cleaned.append(msg)

    return cleaned

# =====================================================
# TOOLS
# =====================================================

tavily_tool = TavilySearchResults(max_results=5)

# =====================================================
# CLASSIFIER NODE
# =====================================================

def classifier_node(state):

    question = state["messages"][-1].content

    route = keyword_router(question)

    if route:
        return {"route": route}

    response = llm.invoke([("system", CLASSIFIER_PROMPT),("human", question)])

    route = str(response.content).strip().lower()

    valid_routes = {
        "law",
        "football_data",
        "worldcup_data",
        "worldcup2026",
        "general_news"
    }

    if route not in valid_routes:
        route = "general_news"

    return {"route": route}

# =====================================================
# LAW NODE
# =====================================================

def law_node(state):
    question = state["messages"][-1].content

    law_context = search_ifab_law.invoke({"question": question})

    response = llm.invoke([
            SystemMessage(
                content=f"""
        Bạn là chuyên gia luật bóng đá IFAB.

        Chỉ sử dụng thông tin sau:

        {law_context}

        Nếu không tìm thấy luật liên quan
        hãy nói rõ.
        """
            ),
            HumanMessage(
                content=question
            )
        ]
    )

    return {"messages": [response]}

# =====================================================
# WORLD CUP HISTORY NODE
# =====================================================

worldcup_tools = [get_world_cup_overview]
worldcup_llm = llm.bind_tools(worldcup_tools)


def worldcup_node(state):
    messages = get_tool_history(state["messages"])

    response = worldcup_llm.invoke([SystemMessage(content=WORLDCUP_PROMPT)] + messages)

    return {"messages": [response]}

# =====================================================
# FOOTBALL NODE
# =====================================================

football_tools = [get_wc_matches,get_match_events,get_match_lineup,get_match_statistics]
football_llm = llm.bind_tools(football_tools)


def football_node(state):
    messages = get_tool_history(state["messages"])

    response = football_llm.invoke([SystemMessage(content=FOOTBALL_PROMPT)] + messages)

    return {"messages": [response]}

# =====================================================
# WORLD CUP 2026 NODE
# =====================================================

worldcup2026_tools = [
    get_wc2026_info,
    get_wc2026_matches,
    get_wc2026_standings,
    get_wc2026_scorers,
    get_wc2026_match_detail,
    get_wc2026_team,
    get_wc2026_team_matches,
    get_wc2026_team_matches_by_date
]

worldcup2026_llm = llm.bind_tools(worldcup2026_tools)

def worldcup2026_node(state):
    messages = get_tool_history(state["messages"])

    response = worldcup2026_llm.invoke(
        [SystemMessage(content=WORLDCUP_2026_PROMPT)]
        + messages
    )

    return {"messages": [response]}
    
# =====================================================
# NEWS NODE
# =====================================================

tools_for_news = [search_latest_news]
news_llm = llm.bind_tools(tools_for_news)


def news_node(state):
    messages = get_tool_history(state["messages"])

    response = news_llm.invoke(
        [SystemMessage(content=NEWS_PROMPT)]
        + messages
    )

    return {"messages": [response]}

# =====================================================
# FALLBACK NODE
# =====================================================

fallback_llm = llm.bind_tools([search_latest_news])

def fallback_node(state):

    question = ""

    for msg in reversed(state["messages"]):

        if isinstance(msg, HumanMessage):
            question = msg.content
            break

    response = fallback_llm.invoke(
        [
            SystemMessage(content=FALLBACK_PROMPT),
            HumanMessage(content=question)
        ]
    )

    return {
        "messages": [response]
    }

# =====================================================
# TOOL NODE
# =====================================================

from langgraph.prebuilt import ToolNode

football_tool_node = ToolNode(football_tools)

worldcup_tool_node = ToolNode(worldcup_tools)

worldcup2026_tool_node = ToolNode(worldcup2026_tools)

news_tool_node = ToolNode(tools_for_news)

# =====================================================
# SUMMARIZE NODE
# =====================================================
from langgraph.graph.message import RemoveMessage

def summarize_node(state):
    messages = state["messages"]
    if len(messages) < 20:
        return {}

    old_summary = state.get("summary", "")

    response = llm.invoke(
        f"""
        Summary cũ:

        {old_summary}

        Hội thoại:

        {messages}

        Hãy tạo summary mới
        ngắn gọn nhưng đầy đủ.
        """
    )

    return {"summary": response.content,"messages": [RemoveMessage(id=m.id) for m in messages[:-5]]}