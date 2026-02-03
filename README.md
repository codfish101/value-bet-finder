# Value Bet Finder

A sports betting utility that scans odds to find positive Expected Value (+EV) opportunities. 
Ideally used to identify mispriced lines compared to a sharp sportsbook (e.g., Pinnacle).

## ⚠️ DISCLAIMER & RESPONSIBLE GAMBLING

**PLEASE READ CAREFULLY:**

1.  **NO GUARANTEES**: Sports betting involves significant risk. Even +EV bets can lose. This tool provides *estimates* based on probability models. It does not guarantee profit.
2.  **NOT FINANCIAL ADVICE**: This software is for educational and entertainment purposes only.
3.  **DATA DELAYS**: Odds change in seconds. The data you see may be stale. Always verify odds on the sportsbook before betting.
4.  **ANTI-HALLUCINATION POLICY**: The system will display "Insufficient Data" or "No Edge" if the math does not strictly support a bet. It does NOT "guess" winners.

**If you or someone you know has a gambling problem, help is available:**
-   **USA**: Call 1-800-GAMBLER (1-800-426-2537)
-   **UK**: GamCare
-   **Canada**: ConnexOntario (1-866-531-2600)

---

## Getting Started (Local Dev)

### Prerequisites
-   Python 3.10+
-   Node.js 18+

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API will be running at `http://localhost:8000`.
Specs: `http://localhost:8000/docs`

### 2. Frontend Setup
```bash
cd frontend
npm run dev
```
App will be running at `http://localhost:3000`.

### 3. Quick Demo (CLI)
You can test the math logic without running the full stack:
```bash
python demo_ev_scan.py
```

## Architecture
-   **Backend**: FastAPI, SQLModel (SQLite).
-   **Frontend**: Next.js, Tailwind CSS.
-   **Math**: 
    -   Implied Prob = 1 / Decimal Odds
    -   Vig Removal: Multiplicative Method
    -   Stake Sizing: Fractional Kelly Criterion (default 0.25x)

## License
MIT
