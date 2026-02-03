'use client';

import React, { useEffect, useState } from 'react';
import EVTable from '@/components/EVTable';
import ParlayCard from '@/components/ParlayCard';
import { BetOpportunity } from '@/types';

export default function Home() {
  const [opportunities, setOpportunities] = useState<BetOpportunity[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchOpportunities();
  }, []);

  const fetchOpportunities = async () => {
    setLoading(true);
    setError(null);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/ev/feed`);
      if (!res.ok) {
        throw new Error('Failed to fetch data');
      }
      const data: BetOpportunity[] = await res.json();
      setOpportunities(data);
    } catch (err) {
      console.error(err);
      setError('Could not connect to API. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-900 text-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-blue-500">
              Value Bet Finder
            </h1>
            <p className="text-gray-400 mt-2">
              Live Positive EV Opportunities • 0.25x Kelly
            </p>
          </div>
          <button
            onClick={fetchOpportunities}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-sm font-semibold transition"
          >
            Refresh Odds
          </button>
        </header>

        {error && (
          <div className="p-4 mb-6 bg-red-900/50 border border-red-500 rounded text-red-200">
            {error}
          </div>
        )}

        {/* Parlay Feature */}
        <ParlayCard />

        {loading ? (
          <div className="text-center py-20">
            <span className="loading-spinner animate-spin text-4xl">⟳</span>
            <p className="mt-4 text-gray-500">Scanning markets...</p>
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
