import json
import os
import sys

# Add backend to path so we can import core modules
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.core.math_logic import to_decimal, remove_vig_multiplicative, calculate_ev, kelly_criterion

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "sample_odds.json")

def main():
    print("----------------------------------------------------------------")
    print(" VALUE BET FINDER (LOCAL DEMO) ")
    print("----------------------------------------------------------------")
    print(f"Loading data from: {DATA_FILE}")
    
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: Sample data not found.")
        return

    print(f"Scanning {len(data)} games for +EV opportunities...\n")
    
    found_bets = 0
    
    print(f"{'MATCH':<35} | {'BOOK':<12} | {'BET':<20} | {'ODDS':<6} | {'EV%':<6} | {'STAKE ($1k)'}")
    print("-" * 110)

    for game in data:
        sharp_book = next((b for b in game["bookmakers"] if b["key"] == "pinnacle"), None)
        if not sharp_book: continue
        
        # Get Sharp H2H
        market = next((m for m in sharp_book["markets"] if m["key"] == "h2h"), None)
        if not market: continue
        
        sharp_outcomes = market["outcomes"]
        sharp_h = to_decimal(sharp_outcomes[0]["price"])
        sharp_a = to_decimal(sharp_outcomes[1]["price"])
        
        fp_h, fp_a = remove_vig_multiplicative(sharp_h, sharp_a)
        
        for book in game["bookmakers"]:
            if book["key"] == "pinnacle": continue
            
            book_market = next((m for m in book["markets"] if m["key"] == "h2h"), None)
            if not book_market: continue
            
            for i, outcome in enumerate(book_market["outcomes"]):
                offered = to_decimal(outcome["price"])
                fair = fp_h if i == 0 else fp_a
                
                ev = calculate_ev(fair, offered)
                
                if ev > 0.5: # Show bets with > 0.5% EV
                    found_bets += 1
                    kelly = kelly_criterion(fair, offered) * 0.25 # Quarter Kelly
                    stake = 1000 * kelly
                    
                    team = outcome["name"]
                    match_str = f"{game['home_team']} vs {game['away_team']}"
                    
                    print(f"{match_str:<35} | {book['title']:<12} | {team:<20} | {outcome['price']:<6} | {ev:5.2f}% | ${stake:6.2f}")

    print("-" * 110)
    print(f"\nScan Complete. Found {found_bets} opportunities.")

if __name__ == "__main__":
    main()
