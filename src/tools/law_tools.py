from langchain_core.tools import tool
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.law_search import query_law

@tool
def search_ifab_law(question: str) -> str:
    """
    Search IFAB Laws of the Game
    using local FAISS database.

    Use this tool when users ask about:

    - Offside
    - Handball
    - Red card
    - Yellow card
    - Penalty
    - VAR
    - Referee decisions
    - FIFA football laws

    Returns relevant IFAB law passages.
    """

    return query_law(question)


