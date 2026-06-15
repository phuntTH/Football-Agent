import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import tool

from services.football_service import (
    get_world_cup_matches,
    get_fixture_events,
    get_fixture_lineups,
    get_fixture_statistics
)


@tool
def get_wc_matches(year: str) -> str:
    """
    Get all World Cup matches.
    """

    data = get_world_cup_matches(year)

    return json.dumps(data["response"], ensure_ascii=False)


@tool
def get_match_events(fixture_id: int) -> str:
    """
    Get goals, cards and substitutions.
    """

    data = get_fixture_events(fixture_id)

    return json.dumps(data["response"], ensure_ascii=False)


@tool
def get_match_lineup(fixture_id: int) -> str:
    """
    Get starting XI and substitutes.
    """

    data = get_fixture_lineups(fixture_id)

    return json.dumps(data["response"], ensure_ascii=False)


@tool
def get_match_statistics(fixture_id: int) -> str:
    """
    Get match statistics.
    """

    data = get_fixture_statistics(fixture_id)

    return json.dumps(data["response"], ensure_ascii=False)