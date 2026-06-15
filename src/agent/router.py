import json
from langchain_core.messages import ToolMessage

# ==================================================
# HYBRID KEYWORD ROUTER
# ==================================================
def keyword_router(question: str):
    q = question.lower()

    # ==================================================
    # DATA KHÔNG CÓ TRONG FOOTBALL-DATA API
    # => ĐI THẲNG TAVILY
    # ==================================================
    if any(k in q for k in [
        "đội hình xuất phát",
        "đội hình ra sân",
        "starting xi",
        "lineup",
        "formation",
        "sơ đồ chiến thuật",
        "squad",
        "danh sách thi đấu"
    ]):
        return "general_news"

    # ==================================================
    # LAW
    # ==================================================
    if any(k in q for k in [
        "việt vị",
        "offside",
        "penalty",
        "var",
        "trọng tài",
        "luật",
        "thẻ đỏ",
        "thẻ vàng",
        "handball"
    ]):
        return "law"

    # ==================================================
    # WORLD CUP 2026
    # ==================================================
    if any(k in q for k in [
        "world cup 2026",
        "wc 2026",
        "vòng loại world cup 2026",
        "lịch thi đấu world cup 2026",
        "bảng xếp hạng world cup 2026",
        "world cup mới nhất"
    ]):
        return "worldcup2026"

    # ==================================================
    # FOOTBALL DATA
    # ==================================================
    if any(k in q for k in [
        "ghi bàn",
        "bàn thắng",
        "kiến tạo",
        "assist",
        "thống kê",
        "tỉ số",
        "kết quả",
        "trận đấu",
        "phút",
        "thẻ phạt",
        "cầu thủ"
    ]):
        return "football_data"

    # ==================================================
    # WORLD CUP HISTORY
    # ==================================================
    if any(k in q for k in [
        "đội vô địch",
        "vua phá lưới",
        "nước chủ nhà",
        "lịch sử world cup",
        "thể thức world cup"
    ]):
        return "worldcup_data"

    return None

# ==================================================
# CLASSIFIER
# ==================================================
def route_classifier(state):
    route = state.get(
        "route",
        "general_news"
    )

    valid = {
        "law",
        "football_data",
        "worldcup_data",
        "worldcup2026",
        "general_news"
    }

    if route not in valid:
        return "general_news"

    return route

# ==================================================
# TOOL ROUTERS
# ==================================================
def route_football_tools(state):
    last = state["messages"][-1]

    if getattr(last, "tool_calls", None):
        return "tool"

    return "summarize"

def route_worldcup_tools(state):
    last = state["messages"][-1]

    if getattr(last, "tool_calls", None):
        return "tool"

    return "summarize"

def route_news_tools(state):
    last = state["messages"][-1]

    if getattr(last, "tool_calls", None):
        return "tool"

    return "summarize"

# ==================================================
# FALLBACK DETECTOR
# ==================================================
def should_fallback(tool_msg: ToolMessage):
    if not isinstance(tool_msg, ToolMessage):
        return False

    content = tool_msg.content

    if not content:
        return True

    text = str(content).strip().lower()

    if text in [
        "",
        "[]",
        "{}",
        "null",
        "none"
    ]:
        return True

    fallback_signals = [
        "not found",
        "no data",
        "no results",
        "không tìm thấy",
        "không có dữ liệu",
        "dữ liệu không tồn tại",
        "fixture not found",
        "player not found"
    ]

    if any(x in text for x in fallback_signals):
        return True

    # ==================================================
    # KIỂM TRA CÁC TOOL THƯỜNG THIẾU DỮ LIỆU
    # ==================================================
    try:
        data = json.loads(content)
    except Exception:
        return False

    tool_name = getattr(tool_msg, "name", "")

    # football-data free không có lineup
    if tool_name == "get_wc2026_match_detail":
        if isinstance(data, dict):
            if "lineups" not in data:
                return True

    return False

# ==================================================
# AFTER FOOTBALL TOOL
# ==================================================
def route_after_football_tool(state):
    last = state["messages"][-1]

    if not isinstance(last, ToolMessage):
        return "football"

    if should_fallback(last):
        return "fallback_news"

    return "football"

# ==================================================
# AFTER WORLDCUP TOOL
# ==================================================
def route_after_worldcup_tool(state):
    last = state["messages"][-1]

    if not isinstance(last, ToolMessage):
        return "worldcup"

    if should_fallback(last):
        return "fallback_news"

    return "worldcup"

# ==================================================
# AFTER WORLDCUP2026 TOOL
# ==================================================
def route_after_worldcup2026_tool(state):
    last = state["messages"][-1]

    if not isinstance(last, ToolMessage):
        return "worldcup2026"

    if should_fallback(last):
        return "fallback_news"

    return "worldcup2026"

# ==================================================
# AFTER NEWS TOOL
# ==================================================
def route_after_news_tool(state):
    return "news"

# ==================================================
# AFTER FALLBACK TOOL
# ==================================================
def route_after_fallback_tool(state):
    return "summarize"