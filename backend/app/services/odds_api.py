import httpx
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4/sports"

async def get_live_odds(sport_key: str = "upcoming", regions: str = "us", markets: str = "h2h") -> List[Dict[str, Any]]:
    """
    Fetch live odds from The Odds API.
    """
    if not API_KEY:
        print("Warning: No ODDS_API_KEY found. Returning empty list.")
        return []

    params = {
        "apiKey": API_KEY,
        "regions": regions,
        "markets": markets,
        "oddsFormat": "decimal",
        "dates": "iso"
    }

    async with httpx.AsyncClient() as client:
        try:
            # First, simply get odds for the requested sport (or default to NBA/Top sports if generic)
            # For MVP, let's hardcode a list of popular sports to iterate if 'upcoming' is vague
            # But the API supports /{sport}/odds
            
            # Using 'upcoming' isn't a valid sport key for the odds endpoint directly typically, 
            # we need specific sport keys.
            
            # Let's target NBA for the demo if 'upcoming' is passed, or just use what is passed.
            target_sport = "basketball_nba" if sport_key == "upcoming" else sport_key
            
            url = f"{BASE_URL}/{target_sport}/odds"
            
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            print(f"API Error: {e.response.status_code} - {e.response.text}")
            return []
        except Exception as e:
            print(f"Network Error: {e}")
            return []
