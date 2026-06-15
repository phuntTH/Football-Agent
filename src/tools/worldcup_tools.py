import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import tool

from services.zafronix_service import (get_tournament)


@tool
def get_world_cup_overview(year: str) -> str:
    """
    Get overview information of a World Cup edition.

    Returns:
    - Host country
    - Champion
    - Runner-up
    - Top scorer
    - Number of teams
    - Number of matches
    - Historical notes
    - Participating teams
    """

    try:
        raw = get_tournament(year)
        tournament = raw.get("tournament", {})
        teams = raw.get("teams", [])

        result = {
            "world_cup": f"World Cup {year}",

            "host": tournament.get("host"),

            "champion": tournament.get("champion"),

            "runner_up": tournament.get("runnerUp"),

            "top_scorer": tournament.get("topScorer"),
            
            "matches_count": tournament.get("matchesCount"),
            
            "teams_count": tournament.get("teamsCount"),
            
            "notes": tournament.get("notes", "Không có ghi chú lịch sử."),
            
            "teams": [team.get("name") for team in teams if team.get("name")]
        }

        return json.dumps(result, indent=4, ensure_ascii=False)

    except Exception as e:
        return json.dumps(
            {
                "error": str(e)
            },
            ensure_ascii=False
        )


if __name__ == "__main__":

    result = get_world_cup_overview.invoke(
        {
            "year": "2022"
        }
    )

    print(result)