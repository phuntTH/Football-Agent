import json

from langchain_core.tools import tool
from langchain_community.tools import TavilySearchResults


tavily = TavilySearchResults(max_results=3,search_depth="advanced",include_raw_content=False)


@tool
def search_latest_news(query: str) -> str:
    """
    Search latest football and World Cup news.

    Use this tool when users ask about:

    - Recent football news
    - Injuries
    - Transfers
    - Squad announcements
    - World Cup 2026 updates
    - Coach interviews
    - FIFA announcements

    Always returns:
    - title
    - summary
    - source url

    The final answer must cite sources.
    """

    results = tavily.invoke(query)

    news = []

    for item in results:

        news.append(
            {"title": item.get("title", ""),
             "summary": item.get("content", ""),
             "url": item.get("url", "")
            }
        )

    return json.dumps(news, ensure_ascii=False, indent=2)