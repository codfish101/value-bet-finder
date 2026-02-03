"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';

type SavedBet = {
    id: number;
    match_name: string;
    selection: string;
    odds: number;
    stake: number;
    ev_percent: number;
    book: string;
    status: string;
};

export default function HistoryPage() {
    const [bets, setBets] = useState<SavedBet[]>([]);

    useEffect(() => {
        const fetchHistory = async () => {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const res = await fetch(`${apiUrl}/history`);
            if (res.ok) {
                const data = await res.json();
                setBets(data);
            }
        };
        fetchHistory();
    }, []);

    return (
        <div className="min-h-screen bg-gray-900 text-white p-8">
            <div className="max-w-7xl mx-auto">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                        My Portfolio
                    </h1>
                    <Link href="/" className="text-blue-400 hover:text-white underline">
                        ← Back to Scanner
                    </Link>
                </div>

                <div className="bg-gray-800 rounded-xl overflow-hidden shadow-xl border border-gray-700">
                    <table className="w-full">
                        <thead className="bg-gray-900">
                            <tr>
                                <th className="p-4 text-left">Match</th>
                                <th className="p-4 text-left">Selection</th>
                                <th className="p-4 text-left">Odds</th>
                                <th className="p-4 text-left">Stake</th>
                                <th className="p-4 text-left">Book</th>
                                <th className="p-4 text-left">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {bets.map((bet) => (
                                <tr key={bet.id} className="border-b border-gray-700">
                                    <td className="p-4 font-bold">{bet.match_name}</td>
                                    <td className="p-4 text-yellow-400">{bet.selection}</td>
                                    <td className="p-4">{bet.odds}</td>
                                    <td className="p-4">${bet.stake.toFixed(2)}</td>
                                    <td className="p-4 text-blue-300">{bet.book}</td>
                                    <td className="p-4">
                                        <span className="px-2 py-1 bg-yellow-900 text-yellow-200 rounded text-xs">
                                            {bet.status}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    {bets.length === 0 && (
                        <div className="p-8 text-center text-gray-500">
                            No bets saved yet. Go to the dashboard and track some value!
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
