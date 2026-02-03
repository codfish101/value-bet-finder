from typing import List, Tuple, Optional

def to_decimal(odds: int) -> float:
    """
    Convert American odds to Decimal odds.
    Example: -110 -> 1.909, +150 -> 2.50
    """
    if odds > 0:
        return 1 + (odds / 100)
    else:
        return 1 + (100 / abs(odds))

def implied_prob(decimal_odds: float) -> float:
    """
    Calculate implied probability from decimal odds.
    """
    if decimal_odds <= 0:
        return 0.0
    return 1 / decimal_odds

def remove_vig_multiplicative(odds_a: float, odds_b: float) -> Tuple[float, float]:
    """
    Remove vig (margin) from a 2-way market using the Multiplicative method.
    This assumes the vig is proportional to the odds.
    
    Args:
        odds_a: Decimal odds for outcome A
        odds_b: Decimal odds for outcome B
        
    Returns:
        Tuple of (Fair Probability A, Fair Probability B)
    """
    ip_a = implied_prob(odds_a)
    ip_b = implied_prob(odds_b)
    
    # Overround (Total Implied Probability)
    S = ip_a + ip_b
    
    if S == 0:
        return 0.0, 0.0
        
    # Fair Probabilities
    fp_a = ip_a / S
    fp_b = ip_b / S
    
    return fp_a, fp_b

def calculate_ev(fair_prob: float, offered_odds: float) -> float:
    """
    Calculate Expected Value percentage.
    
    Args:
        fair_prob: The true probability of winning (0-1)
        offered_odds: The decimal odds currently offered
        
    Returns:
        EV as a percentage (e.g., 5.0 for 5% EV)
    """
    # EV = (Probability of Win * Profit) - (Probability of Loss * Stake)
    # Profit = Stake * (Odds - 1)
    # Stake = 1
    # EV = (P * (Odds - 1)) - ((1-P) * 1)
    # Simplified: EV = (P * Odds) - 1
    
    if fair_prob <= 0 or offered_odds <= 0:
        return 0.0
        
    ev_decimal = (fair_prob * offered_odds) - 1
    return ev_decimal * 100

def kelly_criterion(fair_prob: float, decimal_odds: float, fraction: float = 1.0) -> float:
    """
    Calculate the Kelly Criterion stake sizing fraction.
    
    Args:
        fair_prob: The true probability of winning (p)
        decimal_odds: The decimal odds offered (b + 1)
        fraction: Kelly multiplier (e.g., 0.25 for Quarter Kelly). Default 1.0 (Full Kelly).
        
    Returns:
        Recommended bankroll fraction to bet (0.0 - 1.0)
    """
    if decimal_odds <= 1:
        return 0.0
        
    # b = net odds (odds - 1)
    b = decimal_odds - 1
    p = fair_prob
    q = 1 - p
    
    # f* = (bp - q) / b
    f_star = ((b * p) - q) / b
    
    if f_star < 0:
        return 0.0
        
    return f_star * fraction
