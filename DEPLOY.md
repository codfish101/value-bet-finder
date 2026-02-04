# Deployment Guide (Version 2.0)

Your app now includes a **Database** to save bets. This means deployments have one extra step.

## 1. The Database (PostgreSQL) -> Render.com
1.  Log in to [Render.com](https://render.com).
2.  Click **New +** -> **PostgreSQL**.
3.  **Name**: `vbf-db` (or anything).
4.  **Region**: Pick the same one you will use for the web service (e.g., "Ohio" or "Frankfurt").
5.  **Plan**: "Free".
6.  Click **Create Database**.
7.  **Wait** for it to finish.
8.  Find the **"Internal Database URL"** (starts with `postgres://...`). **Copy this.**

## 2. The Backend (Python API) -> Render.com
1.  Click **New +** -> **Web Service**.
2.  Connect your GitHub repo.
3.  **Settings**:
    -   **Root Directory**: `backend`
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
4.  **Environment Variables** (Advanced):
    -   Key: `ODDS_API_KEY` -> Value: `Your_Key_Here`
    -   Key: `DATABASE_URL` -> Value: **Paste the Internal DB URL you copied above.**
5.  Click **Deploy**.
6.  Once live, copy the URL (e.g., `https://value-bet-finder.onrender.com`).

## 3. The Frontend (Next.js) -> Vercel
1.  Go to [Vercel.com](https://vercel.com).
2.  Click **Add New...** -> **Project**.
3.  Connect the same GitHub repo.
4.  **Settings**:
    -   **Root Directory**: `frontend`
    -   **Environment Variables**:
        -   Key: `NEXT_PUBLIC_API_URL`
        -   Value: `https://value-bet-finder.onrender.com` (Your Render Backend URL).
5.  Click **Deploy**.

## 4. Done!
Vercel will give you a link (e.g., `value-bet-finder.vercel.app`).
**You can now track bets, and they will be saved to your cloud database forever!**
