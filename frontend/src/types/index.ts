export interface BetOpportunity {
  match_name: string;
  sport: string;
  market: string;
  selection: string;
  target_book: string;
  target_odds_american: number;
  target_odds_decimal: number;
  sharp_book: string;
  sharp_odds_decimal: number[];
  fair_prob: number;
  ev_percent: number;
  kelly_fraction: number;
  kelly_stake_suggested: number;
  timestamp: string;
}
