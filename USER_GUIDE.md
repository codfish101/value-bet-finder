# Value Bet Finder - Quick Start Guide

## 🎯 What This App Does

The Value Bet Finder scans live sports betting odds from 40+ bookmakers and identifies **positive Expected Value (+EV)** opportunities by comparing them against sharp bookmaker lines (Pinnacle). It helps you find mathematically advantageous bets across multiple sports.

### Features:
- ✅ **Live Odds Data** from The Odds API
- ✅ **Multi-Sport Support** (NBA, NFL, MLB, NHL, Soccer)
- ✅ **EV Calculation** with vig removal
- ✅ **Kelly Criterion** stake sizing
- ✅ **Bet Tracking** with PostgreSQL database
- ✅ **Parlay Generator** for high-odds tickets

---

## 🚀 Getting Started

### Step 1: Get a Free API Key

1. Visit [The Odds API](https://the-odds-api.com/)
2. Sign up for a free account
3. Copy your API key (you get 500 requests/month free)

### Step 2: Run Locally

#### Backend:
```bash
cd backend
pip install -r requirements.txt

# Create .env file
echo "ODDS_API_KEY=your_key_here" > .env

# Start the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

#### Frontend:
```bash
cd frontend
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start the dev server
npm run dev
```

The app will be available at `http://localhost:3000`

---

## 🌐 Deploy to Production

### Option 1: Deploy with Render + Vercel (Recommended)

#### A. Deploy Backend to Render

1. **Create PostgreSQL Database**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click **New** → **PostgreSQL**
   - Name: `vbf-database`
   - Plan: Free
   - Click **Create Database**
   - Copy the **Internal Database URL**

2. **Deploy Backend API**
   - Click **New** → **Web Service**
   - Connect your GitHub repository
   - Settings:
     - **Name**: `value-bet-finder-api`
     - **Root Directory**: `backend`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     - `ODDS_API_KEY` = `your_api_key_here`
     - `DATABASE_URL` = `paste_internal_database_url_here`
     - `FRONTEND_URL` = `https://your-app.vercel.app` (add after deploying frontend)
   - Click **Create Web Service**
   - Copy your backend URL (e.g., `https://value-bet-finder-api.onrender.com`)

#### B. Deploy Frontend to Vercel

1. **Deploy to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click **Add New** → **Project**
   - Import your GitHub repository
   - Settings:
     - **Root Directory**: `frontend`
     - **Framework Preset**: Next.js
   - Environment Variables:
     - `NEXT_PUBLIC_API_URL` = `https://value-bet-finder-api.onrender.com`
   - Click **Deploy**

2. **Update Backend CORS**
   - Go back to Render dashboard
   - Add environment variable:
     - `FRONTEND_URL` = `https://your-app.vercel.app`
   - Restart the backend service

### Option 2: Use Infrastructure-as-Code

We've included `render.yaml` for automated Render deployment:

```bash
# Push to GitHub
git add .
git commit -m "Ready for deployment"
git push

# In Render dashboard, create "New Blueprint Instance"
# Point it to your repo - it will auto-configure everything!
```

---

## 📊 Using the App

### Understanding the Data

- **EV %**: Expected Value percentage. Positive = good bet opportunity
- **Kelly Stake**: Recommended bet size based on 0.25x fractional Kelly (conservative)
- **Fair Prob**: True probability after removing bookmaker vig
- **Sharp Odds**: Pinnacle's odds (used as the "truth" baseline)

### Sport Selection

Use the dropdown to switch between:
- 🏀 NBA Basketball
- 🏈 NFL Football  
- ⚾ MLB Baseball
- 🏒 NHL Hockey
- ⚽ Premier League
- ⚽ Champions League

### Tracking Bets

1. Click **Track** on any opportunity
2. View your portfolio at `/history`
3. Bets are saved permanently in the database

---

## ⚠️ Important Notes

### API Usage Limits

The free tier includes **500 requests/month**. The app caches data for 5 minutes to conserve requests.

**Estimated usage:**
- Each page load = 1 request
- Switching sports = 1 request
- Cache duration = 5 minutes

**Tip**: Don't refresh too frequently! The odds don't change that fast.

### Responsible Gambling

- This tool provides **estimates**, not guarantees
- Even +EV bets can lose
- Never bet money you can't afford to lose
- If you have a gambling problem, call **1-800-GAMBLER**

### Data Freshness

- Odds can change in seconds
- Always verify odds on the actual sportsbook before placing a bet
- The "Last updated" timestamp shows when data was fetched

---

## 🛠️ Troubleshooting

### "No API key configured"
- Make sure `ODDS_API_KEY` is set in your environment variables
- Check the `/health` endpoint to verify configuration

### "Failed to fetch data"
- Check that the backend is running
- Verify `NEXT_PUBLIC_API_URL` is set correctly in frontend
- Check browser console for CORS errors

### "No +EV opportunities found"
- This is normal! Not all sports have +EV bets at all times
- Try a different sport
- Refresh the data (odds may have changed)

### API quota exceeded
- Check your usage at [The Odds API Dashboard](https://the-odds-api.com/account/)
- The app will use cached data when quota is exceeded
- Consider upgrading to a paid plan if needed

---

## 📚 Additional Resources

- [The Odds API Documentation](https://the-odds-api.com/liveapi/guides/v4/)
- [Kelly Criterion Explained](https://en.wikipedia.org/wiki/Kelly_criterion)
- [Expected Value in Sports Betting](https://www.pinnacle.com/en/betting-articles/betting-strategy/expected-value-in-betting)

---

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the `/docs` endpoint on your backend
3. Check the browser console for errors

**Good luck finding value!** 🎰📈
