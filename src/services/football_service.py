import requests
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


from config import API_FOOTBALL_KEY


BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {"x-apisports-key": API_FOOTBALL_KEY}


def football_get(endpoint: str, params: dict | None = None):
    response = requests.get(f"{BASE_URL}/{endpoint}",headers=HEADERS, params=params, timeout=20)

    response.raise_for_status()

    return response.json()


def get_world_cup_matches(season: str):
    return football_get(
        "fixtures",
        {
            "league": 1,
            "season": season
        }
    )


def get_fixture_lineups(fixture_id: int
):
    return football_get(
        "fixtures/lineups",
        {
            "fixture": fixture_id
        }
    )


def get_fixture_events(fixture_id: int):
    return football_get(
        "fixtures/events",
        {
            "fixture": fixture_id
        }
    )


def get_fixture_statistics(fixture_id: int):
    return football_get(
        "fixtures/statistics",
        {
            "fixture": fixture_id
        }
    )