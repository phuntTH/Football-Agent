import requests
import os
import sys

from datetime import datetime, timedelta

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from config import FOOTBALL_DATA_API_KEY


BASE_URL = "https://api.football-data.org/v4"

HEADERS = {
    "X-Auth-Token": FOOTBALL_DATA_API_KEY
}


# =====================================================
# UTC -> VIETNAM TIME
# =====================================================

def _convert_utc_to_vietnam(obj):

    if isinstance(obj, dict):

        for key, value in list(obj.items()):

            if (
                key == "utcDate"
                and isinstance(value, str)
            ):

                try:

                    dt = datetime.fromisoformat(
                        value.replace("Z", "+00:00")
                    )

                    vn_time = dt + timedelta(hours=7)

                    obj["matchTimeVN"] = vn_time.strftime(
                        "%Y-%m-%d %H:%M:%S (GMT+7)"
                    )

                except Exception:
                    pass

            else:
                _convert_utc_to_vietnam(value)

    elif isinstance(obj, list):

        for item in obj:
            _convert_utc_to_vietnam(item)

    return obj


# =====================================================
# REQUEST
# =====================================================

def _get(endpoint: str):

    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    return _convert_utc_to_vietnam(data)


# =====================================================
# WORLD CUP
# =====================================================

def get_world_cup_info():

    return _get(
        "/competitions/WC"
    )


def get_world_cup_matches():

    return _get(
        "/competitions/WC/matches"
    )


def get_world_cup_standings():

    return _get(
        "/competitions/WC/standings"
    )


def get_world_cup_scorers():

    return _get(
        "/competitions/WC/scorers"
    )


# =====================================================
# FILTER MATCHES
# =====================================================

def get_matches_by_date(
    date_from: str,
    date_to: str
):

    return _get(
        f"/competitions/WC/matches"
        f"?dateFrom={date_from}"
        f"&dateTo={date_to}"
    )


# =====================================================
# MATCH
# =====================================================

def get_match(
    match_id: int
):

    return _get(
        f"/matches/{match_id}"
    )


# =====================================================
# TEAM
# =====================================================

def get_team(
    team_id: int
):

    return _get(
        f"/teams/{team_id}"
    )


def get_team_matches(
    team_id: int
):

    return _get(
        f"/teams/{team_id}/matches"
    )


def get_team_matches_by_date(
    team_id: int,
    date_from: str,
    date_to: str
):

    return _get(
        f"/teams/{team_id}/matches"
        f"?dateFrom={date_from}"
        f"&dateTo={date_to}"
    )