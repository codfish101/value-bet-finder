import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application configuration settings"""
    
    # API Configuration
    ODDS_API_KEY: Optional[str] = os.getenv("ODDS_API_KEY")
    ODDS_API_BASE_URL: str = "https://api.the-odds-api.com/v4/sports"
    
    # Database Configuration
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # Default to SQLite for local development
    if not DATABASE_URL:
        DATABASE_URL = "sqlite:///./bets.db"
    
    # CORS Configuration
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        FRONTEND_URL
    ]
    
    # Add Vercel preview URLs pattern
    if "vercel.app" in FRONTEND_URL:
        ALLOWED_ORIGINS.append("https://*.vercel.app")
    
    # Application Settings
    APP_NAME: str = "Value Bet Finder API"
    APP_VERSION: str = "2.0.0"
    
    # Sports Configuration
    SUPPORTED_SPORTS: dict = {
        "basketball_nba": "NBA Basketball",
        "americanfootball_nfl": "NFL Football",
        "baseball_mlb": "MLB Baseball",
        "icehockey_nhl": "NHL Hockey",
        "soccer_epl": "English Premier League",
        "soccer_uefa_champs_league": "UEFA Champions League"
    }
    
    # API Settings
    DEFAULT_REGIONS: str = "us"
    DEFAULT_MARKETS: str = "h2h,spreads,totals"
    ODDS_FORMAT: str = "decimal"
    
    # Rate Limiting (for future implementation)
    MAX_REQUESTS_PER_MINUTE: int = 10
    
    def validate(self) -> list[str]:
        """Validate configuration and return list of warnings/errors"""
        issues = []
        
        if not self.ODDS_API_KEY or len(self.ODDS_API_KEY) < 10:
            issues.append("⚠️  ODDS_API_KEY not configured - will use sample data only")
        
        if "sqlite" in self.DATABASE_URL.lower():
            issues.append("ℹ️  Using SQLite database (local development mode)")
        else:
            issues.append(f"✓ Using PostgreSQL database")
        
        return issues

settings = Settings()
