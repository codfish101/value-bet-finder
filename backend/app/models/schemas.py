from pydantic import BaseModel
from typing import Optional, List

# --- API Models ---

class BetOpportunity(BaseModel):
    match_name: str
    sport: str
    market: str  # e.g., "Moneyline", "Spread -3.5"
    selection: str # e.g. "Lakers", "Over 210.5"
    
    # The Book we are betting on
    target_book: str
    target_odds_american: int
    target_odds_decimal: float
    
    # The Sharp Book (Reference)
    sharp_book: str
    sharp_odds_decimal: List[float] # [Home, Away] or similar
    
    # Math
    fair_prob: float        # True win probability (0-1)
    ev_percent: float       # Expected Value %
    kelly_fraction: float   # Recommended stake % (Full Kelly)
    kelly_stake_suggested: float # Example stake for $1000 bankroll (0.25 Kelly)
    
    timestamp: str

class ParlayLeg(BaseModel):
    match_name: str
    sport: str
    market: str
    selection: str
    odds_american: int
    odds_decimal: float
    ev_percent: float

class ParlayRecommendation(BaseModel):
    book: str
    total_odds_decimal: float
    total_odds_american: int
    legs: List[ParlayLeg]
    expected_value_combined: float
    note: str

class OddsRequest(BaseModel):
    provider: str = "mock" # "mock" or "the-odds-api"
