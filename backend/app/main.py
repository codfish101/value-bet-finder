from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.math_logic import to_decimal, remove_vig_multiplicative, calculate_ev, kelly_criterion
from app.models.schemas import BetOpportunity, SavedBet
from app.services.odds_api import get_live_odds
from app.core.db import create_db_and_tables, get_session
from sqlmodel import Session, select
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Value Bet Finder API", version="2.0.0")

@app.on_event("startup")
def on_startup():
    try:
        create_db_and_tables()
        print("Database connected and tables created.")
    except Exception as e:
        print(f"CRITICAL DATABASE ERROR: {e}")
        # We don't raise here so the app can start and we can see the logs
        pass

app.add_middleware(
    CORSMiddleware,
    # In production, restrict this to your frontend domain (e.g. vercel.app)
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load sample data path
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "sample_odds.json")

def process_odds_data(data: list) -> list[BetOpportunity]:
    opportunities = []
    
    # Helper to map market keys
    def market_key_to_name(key: str, outcome: dict) -> str:
        if key == "h2h": return "Moneyline"
        if key == "spreads": return f"Spread {outcome.get('point', '')}"
        if key == "totals": return f"Total {outcome.get('point', '')}"
        if "player" in key: return "Player Prop"
        return key

    for game in data:
        # 1. Find the Sharp Book (Pinnacle) to establish "Truth"
        sharp_book = next((b for b in game["bookmakers"] if b["key"] == "pinnacle"), None)
        if not sharp_book:
            continue
            
        # Iterate over all markets in the sharp book to find value in various places
        for sharp_market in sharp_book["markets"]:
            market_key = sharp_market["key"]
            
            # For MVP simplicity, we focus on markets with 2 outcomes per set (ML, Spread, Totals, Player Props)
            outcomes = sharp_market["outcomes"]
            if len(outcomes) != 2:
                continue

            # Convert Sharp odds to Decimal
            def ensure_decimal(p):
                if abs(p) >= 100 or p < 0: return to_decimal(p)
                return p

            # Map outcomes to names
            fp_map = {}
            try:
                sharp_1_dec = ensure_decimal(outcomes[0]["price"])
                sharp_2_dec = ensure_decimal(outcomes[1]["price"])
                
                fp_1, fp_2 = remove_vig_multiplicative(sharp_1_dec, sharp_2_dec)
                
                fp_map[outcomes[0]["name"]] = fp_1
                fp_map[outcomes[1]["name"]] = fp_2
            except IndexError:
                continue

            # 2. Compare against every other book
            for book in game["bookmakers"]:
                if book["key"] == "pinnacle":
                    continue 

                book_market = next((m for m in book["markets"] if m["key"] == market_key), None)
                if not book_market:
                    continue
                    
                for outcome in book_market["outcomes"]:
                    sel_name = outcome["name"]
                    if sel_name not in fp_map:
                        continue 
                        
                    offered_price = outcome["price"]
                    offered_dec = ensure_decimal(offered_price)
                    my_fair_prob = fp_map[sel_name]
                    
                    ev = calculate_ev(my_fair_prob, offered_dec)
                    
                    if ev > 0:
                        kelly_full = kelly_criterion(my_fair_prob, offered_dec)
                        kelly_fraction = kelly_full * 0.25
                        stake = 1000 * kelly_fraction
                        
                        opp = BetOpportunity(
                            match_name=f"{game['home_team']} vs {game['away_team']}",
                            sport=game["sport_key"],
                            market=market_key_to_name(market_key, outcome),
                            selection=sel_name,
                            target_book=book["title"],
                            target_odds_american=int(offered_price) if abs(offered_price) >= 100 else 0,
                            target_odds_decimal=round(offered_dec, 3),
                            sharp_book="Pinnacle",
                            sharp_odds_decimal=[round(sharp_1_dec, 3), round(sharp_2_dec, 3)],
                            fair_prob=round(my_fair_prob, 4),
                            ev_percent=round(ev, 2),
                            kelly_fraction=round(kelly_fraction, 4),
                            kelly_stake_suggested=round(stake, 2),
                            timestamp=datetime.now().isoformat()
                        )
                        opportunities.append(opp)
    
    # Sort
    opportunities.sort(key=lambda x: x.ev_percent, reverse=True)
    return opportunities


@app.get("/")
def read_root():
    return {"status": "active", "system": "Value Bet Finder v1"}

@app.get("/ev/feed", response_model=list[BetOpportunity])
async def get_ev_feed():
    """
    Scans for +EV opportunities.
    Prioritizes LIVE API if network/key available, else falls back to SAMPLE data.
    """
    api_key = os.getenv("ODDS_API_KEY")
    use_live = False
    data = []

    if api_key and len(api_key) > 5:
        # Try Live
        print("Attempting to fetch LIVE data...")
        # Fetch generic NBA for MVP
        data = await get_live_odds(sport_key="basketball_nba")
        if data:
            use_live = True
            print(f"Fetched {len(data)} live games.")
        else:
            print("Live fetch failed (or empty). Falling back to sample.")
    
    if not use_live:
        print("Using SAMPLE data.")
        if not os.path.exists(DATA_FILE):
             raise HTTPException(status_code=404, detail="Sample data not found")
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

    return process_odds_data(data)

from typing import Optional
from app.models.schemas import ParlayRecommendation, ParlayLeg

@app.get("/ev/parlay", response_model=Optional[ParlayRecommendation])
async def get_suggested_parlay(target_book: str = "FanDuel", min_odds: float = 20.0):
    """
    Generates a high-value parlay (Lotto Ticket) for a specific book.
    Targeting ~20x odds.
    """
    # 1. Get all opportunities
    opportunities = await get_ev_feed()
    
    # 2. Filter by Book and Positive EV
    candidates = [
        op for op in opportunities 
        if start_case_insensitive_match(op.target_book, target_book) and op.ev_percent > 0
    ]
    
    # 3. Sort by robustness (EV)
    candidates.sort(key=lambda x: x.ev_percent, reverse=True)
    
    selected_legs = []
    current_combined_odds = 1.0
    used_matches = set()
    
    for bet in candidates:
        # Avoid correlation (Same Game Parlays are complex, so we stick to 1 leg per game for MVP)
        if bet.match_name in used_matches:
            continue
            
        selected_legs.append(bet)
        used_matches.add(bet.match_name)
        current_combined_odds *= bet.target_odds_decimal
        
        if current_combined_odds >= min_odds:
            break
            
    if not selected_legs or current_combined_odds < 2.0:
        return None
        
    # Convert combined odds to American
    if current_combined_odds >= 2.0:
        total_us = int((current_combined_odds - 1) * 100)
    else:
        total_us = int(-100 / (current_combined_odds - 1))
        
    # Create Response
    recommendation = ParlayRecommendation(
        book=target_book,
        total_odds_decimal=round(current_combined_odds, 2),
        total_odds_american=total_us,
        expected_value_combined=sum(leg.ev_percent for leg in selected_legs), # Rough approximation
        note="Parlay built from uncorrelated +EV bets. Variance is high.",
        legs=[
            ParlayLeg(
                match_name=leg.match_name,
                sport=leg.sport,
                market=leg.market,
                selection=get_selection_name(leg),
                odds_american=leg.target_odds_american,
                odds_decimal=leg.target_odds_decimal,
                ev_percent=leg.ev_percent
            ) for leg in selected_legs
        ]
    )
    return recommendation

def start_case_insensitive_match(s1, s2):
    return s1.lower().startswith(s2.lower()) or s2.lower().startswith(s1.lower())

def get_selection_name(op: BetOpportunity) -> str:
    return op.selection

# --- V2: Database Endpoints ---

@app.post("/bets", response_model=SavedBet)
def save_bet(bet: SavedBet, session: Session = Depends(get_session)):
    """
    Save a selected bet to the database (Portfolio).
    """
    session.add(bet)
    session.commit()
    session.refresh(bet)
    return bet

@app.get("/history", response_model=list[SavedBet])
def get_bet_history(session: Session = Depends(get_session)):
    """
    Retrieve all saved bets.
    """
    statement = select(SavedBet).order_by(SavedBet.id.desc())
    results = session.exec(statement)
    return results.all()




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

