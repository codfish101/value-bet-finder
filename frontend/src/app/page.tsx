'use client';

import React, { useEffect, useState } from 'react';
import EVTable from '@/components/EVTable';
import ParlayCard from '@/components/ParlayCard';
import { BetOpportunity } from '@/types';

const SPORTS = {
  'basketball_nba': '🏀 NBA Basketball',
  'americanfootball_nfl': '🏈 NFL Football',
  'baseball_mlb': '⚾ MLB Baseball',
  'icehockey_nhl': '🏒 NHL Hockey',
  'soccer_epl': '⚽ Premier League',
  'soccer_uefa_champs_league': '⚽ Champions League'
};

export default function Home() {
  const [opportunities, setOpportunities] = useState<BetOpportunity[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSport, setSelectedSport] = useState<string>('basketball_nba');
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  useEffect(() => {
    fetchOpportunities();
  }, [selectedSport]);

  const fetchOpportunities = async () => {
    setLoading(true);
    setError(null);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/ev/feed?sport=${selectedSport}`);
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(errorData.detail || 'Failed to fetch data');
      }
      const data: BetOpportunity[] = await res.json();
      setOpportunities(data);
      setLastUpdated(new Date());
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Could not connect to API. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (date: Date | null) => {
    if (!date) return '';
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return 'Just now';
    if (diffMins === 1) return '1 minute ago';
    if (diffMins < 60) return `${diffMins} minutes ago`;
    return date.toLocaleTimeString();
  };

  return (
    <main className="min-h-screen bg-gray-900 text-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-blue-500">
                Value Bet Finder
              </h1>
              <p className="text-gray-400 mt-2">
                Live Positive EV Opportunities • 0.25x Kelly
              </p>
              {lastUpdated && (
                <p className="text-xs text-gray-500 mt-1">
                  📡 Last updated: {formatTimestamp(lastUpdated)}
                </p>
              )}
            </div>
            <div className="flex gap-4">
              <a href="/history" className="px-4 py-2 bg-gray-800 hover:bg-gray-700 border border-gray-600 rounded text-sm font-semibold transition">
                📂 Portfolio
              </a>
              <button
                onClick={fetchOpportunities}
                disabled={loading}
                className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-sm font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? '⟳ Loading...' : '🔄 Refresh'}
              </button>
            </div>
          </div>

          {/* Sport Selector */}
          <div className="flex items-center gap-3 mb-4">
            <label htmlFor="sport-select" className="text-sm font-semibold text-gray-400">
              Sport:
            </label>
            <select
              id="sport-select"
              value={selectedSport}
              onChange={(e) => setSelectedSport(e.target.value)}
              className="px-4 py-2 bg-gray-800 border border-gray-600 rounded text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-green-500 transition"
            >
              {Object.entries(SPORTS).map(([key, label]) => (
                <option key={key} value={key}>
                  {label}
                </option>
              ))}
            </select>
            <span className="text-xs text-gray-500">
              {opportunities.length} opportunities found
            </span>
          </div>
        </header>

        {error && (
          <div className="p-4 mb-6 bg-red-900/50 border border-red-500 rounded text-red-200">
            <p className="font-semibold">⚠️ Error</p>
            <p className="text-sm mt-1">{error}</p>
          </div>
        )}

        {/* Parlay Feature */}
        <ParlayCard />

        {loading ? (
          <div className="text-center py-20">
            <span className="loading-spinner animate-spin text-4xl">⟳</span>
            <p className="mt-4 text-gray-500">Scanning markets...</p>
          </div>
        ) : opportunities.length === 0 ? (
          <div className="text-center py-20 bg-gray-800/50 rounded-lg border border-gray-700">
            <p className="text-2xl mb-2">📊</p>
            <p className="text-gray-400">No +EV opportunities found for this sport right now.</p>
            <p className="text-sm text-gray-500 mt-2">Try refreshing or selecting a different sport.</p>
          </div>
        ) : (
          <EVTable opportunities={opportunities} />
        )}

        <footer className="mt-12 border-t border-gray-800 pt-8 text-center text-xs text-gray-500">
          <p className="font-bold mb-2">RESPONSIBLE GAMBLING DISCLAIMER</p>
          <p className="max-w-2xl mx-auto">
            Sports betting involves risk. This tool provides statistical estimates based on past data and market efficiency models.
            There are NO guarantees of profit. Do not bet money you cannot afford to lose.
          </p>
          <p className="mt-2">
            If you or someone you know has a gambling problem, call 1-800-GAMBLER.
          </p>
        </footer>
      </div>
    </main>
  );
}
