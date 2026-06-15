import os
from dotenv import load_dotenv

load_dotenv()

# GEMINI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# TAVILY
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ZAFRONIX
ZAFRONIX_API_KEY = os.getenv("ZAFRONIX_API_KEY")

# API FOOTBALL
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")

FOOTBALL_DATA_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")