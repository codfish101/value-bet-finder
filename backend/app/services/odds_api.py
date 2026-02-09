import httpx
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4/sports"

# Simple in-memory cache to avoid hitting API limits
_cache: Dict[str, tuple[List[Dict[str, Any]], datetime]] = {}
CACHE_DURATION_MINUTES = 5

async def get_live_odds(
    sport_key: str = "basketball_nba", 
    regions: str = "us", 
    markets: str = "h2h,spreads,totals",
    use_cache: bool = True
) -> List[Dict[str, Any]]:
    """
    Fetch live odds from The Odds API with caching support.
    
    Args:
        sport_key: Sport identifier (e.g., 'basketball_nba', 'americanfootball_nfl')
        regions: Regions to fetch odds for (default: 'us')
        markets: Markets to fetch (default: 'h2h,spreads,totals')
        use_cache: Whether to use cached data if available
    
    Returns:
        List of game odds data
    """
    if not API_KEY or len(API_KEY) < 10:
        print("⚠️  Warning: No valid ODDS_API_KEY found. Returning empty list.")
        return []
    
    # Check cache first
    cache_key = f"{sport_key}_{regions}_{markets}"
    if use_cache and cache_key in _cache:
        cached_data, cached_time = _cache[cache_key]
        if datetime.now() - cached_time < timedelta(minutes=CACHE_DURATION_MINUTES):
            print(f"✓ Using cached data for {sport_key} (age: {(datetime.now() - cached_time).seconds}s)")
            return cached_data

    params = {
        "apiKey": API_KEY,
        "regions": regions,
        "markets": markets,
        "oddsFormat": "decimal",
        "dateFormat": "iso"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            url = f"{BASE_URL}/{sport_key}/odds"
            
            print(f"🔄 Fetching live odds for {sport_key}...")
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Check remaining requests from headers
            remaining = response.headers.get("x-requests-remaining")
            used = response.headers.get("x-requests-used")
            
            if remaining:
                print(f"📊 API Usage: {used} used, {remaining} remaining")
                if int(remaining) < 50:
                    print(f"⚠️  WARNING: Only {remaining} API requests remaining!")
            
            # Cache the result
            _cache[cache_key] = (data, datetime.now())
            
            print(f"✓ Fetched {len(data)} games for {sport_key}")
            return data
            
        except httpx.HTTPStatusError as e:
            error_detail = ""
            try:
                error_detail = e.response.json()
            except:
                error_detail = e.response.text
            
            print(f"❌ API Error ({e.response.status_code}): {error_detail}")
            
            if e.response.status_code == 401:
                print("🔑 Invalid API key. Please check your ODDS_API_KEY environment variable.")
            elif e.response.status_code == 429:
                print("⏱️  Rate limit exceeded. Using cached data if available.")
                # Return cached data even if expired
                if cache_key in _cache:
                    cached_data, _ = _cache[cache_key]
                    return cached_data
            
            return []
            
        except httpx.TimeoutException:
            print(f"⏱️  Request timeout for {sport_key}. Check your internet connection.")
            return []
            
        except Exception as e:
            print(f"❌ Unexpected error: {type(e).__name__}: {e}")
            return []


async def get_available_sports() -> List[Dict[str, Any]]:
    """
    Fetch list of available sports from The Odds API.
    
    Returns:
        List of available sports with their keys and details
    """
    if not API_KEY or len(API_KEY) < 10:
        print("⚠️  Warning: No valid ODDS_API_KEY found.")
        return []
    
    params = {"apiKey": API_KEY}
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            url = BASE_URL
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error fetching sports list: {e}")
            return []


def clear_cache():
    """Clear the odds data cache"""
    global _cache
    _cache = {}
    print("🗑️  Cache cleared")
