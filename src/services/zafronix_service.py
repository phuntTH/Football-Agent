import requests
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config import ZAFRONIX_API_KEY


BASE_URL = "https://api.zafronix.com/fifa/worldcup/v1"

HEADERS = {"X-API-Key": ZAFRONIX_API_KEY}


def get_tournament(year: str):
    response = requests.get(f"{BASE_URL}/tournaments/{year}", headers=HEADERS, timeout=20)
    response.raise_for_status()

    return response.json()