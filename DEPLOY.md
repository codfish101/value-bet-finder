# Deployment Guide

To let other people use your Value Bet Finder (on their phones or computers), you need to host it on the cloud.

Here is the free/easy path:

## 1. The Backend (Python API) -> Render.com
1.  Push your code to GitHub.
2.  Go to [Render.com](https://render.com) (Create Account).
3.  Click **New +** -> **Web Service**.
4.  Connect your GitHub repo.
5.  **Settings**:
    -   **Root Directory**: `backend`
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
    -   **Environment Variables**: Add `ODDS_API_KEY` with your key.
6.  Click **Deploy**. Render will give you a URL like: `https://value-bet-finder.onrender.com`.

## 2. The Frontend (Next.js) -> Vercel
1.  Go to [Vercel.com](https://vercel.com) (Create Account).
2.  Click **Add New...** -> **Project**.
3.  Connect the same GitHub repo.
4.  **Settings**:
    -   **Root Directory**: `frontend`
    -   **Framework**: Next.js (Auto-detected).
    -   **Environment Variables**:
        -   Name: `NEXT_PUBLIC_API_URL`
        -   Value: `https://value-bet-finder.onrender.com` (The URL Render gave you in step 1 WITHOUT the trailing slash).
5.  Click **Deploy**.

## 3. Done!
Vercel will give you a link (e.g., `value-bet-finder.vercel.app`).
You can text this link to anyone, and they can open it on their phone!
