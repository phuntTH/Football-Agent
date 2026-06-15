import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import tool

from services.worldcup2026_service import (
    get_world_cup_info,
    get_world_cup_matches,
    get_world_cup_standings,
    get_world_cup_scorers,
    get_match,
    get_team,
    get_team_matches,
    get_team_matches_by_date
)


# =====================================================
# WORLD CUP INFO
# =====================================================

@tool
def get_wc2026_info() -> str:
    """
    Get World Cup competition information.
    """

    data = get_world_cup_info()

    return json.dumps(
        data,
        ensure_ascii=False
    )


# =====================================================
# MATCHES
# =====================================================

@tool
def get_wc2026_matches() -> str:
    """
    Get all World Cup matches.
    """

    data = get_world_cup_matches()

    return json.dumps(
        data.get("matches", []),
        ensure_ascii=False
    )


# =====================================================
# STANDINGS
# =====================================================

@tool
def get_wc2026_standings() -> str:
    """
    Get World Cup standings.
    """

    data = get_world_cup_standings()

    return json.dumps(
        data,
        ensure_ascii=False
    )


# =====================================================
# TOP SCORERS
# =====================================================

@tool
def get_wc2026_scorers() -> str:
    """
    Get World Cup top scorers.
    """

    data = get_world_cup_scorers()

    return json.dumps(
        data.get("scorers", []),
        ensure_ascii=False
    )


# =====================================================
# MATCH DETAIL
# =====================================================

@tool
def get_wc2026_match_detail(
    match_id: int
) -> str:
    """
    Get match detail by match id.
    """

    data = get_match(match_id)

    return json.dumps(
        data,
        ensure_ascii=False
    )


# =====================================================
# TEAM DETAIL
# =====================================================

@tool
def get_wc2026_team(
    team_id: int
) -> str:
    """
    Get team information.
    """

    data = get_team(team_id)

    return json.dumps(
        data,
        ensure_ascii=False
    )


# =====================================================
# TEAM MATCHES
# =====================================================

@tool
def get_wc2026_team_matches(
    team_id: int
) -> str:
    """
    Get matches of a team.
    """

    data = get_team_matches(team_id)

    return json.dumps(
        data,
        ensure_ascii=False
    )


# =====================================================
# TEAM MATCHES DATE RANGE
# =====================================================

@tool
def get_wc2026_team_matches_by_date(
    team_id: int,
    date_from: str,
    date_to: str
) -> str:
    """
    Get matches of a team in a date range.

    Example:
    date_from = 2026-06-01
    date_to = 2026-06-30
    """

    data = get_team_matches_by_date(
        team_id,
        date_from,
        date_to
    )

    return json.dumps(
        data,
        ensure_ascii=False
    )