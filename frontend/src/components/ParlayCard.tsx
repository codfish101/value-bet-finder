import React, { useEffect, useState } from 'react';

type ParlayLeg = {
    match_name: string;
    selection: string;
    odds_american: number;
    ev_percent: number;
    market: string;
};

type ParlayRecommendation = {
    book: string;
    total_odds_american: number;
    total_odds_decimal: number;
    expected_value_combined: number;
    legs: ParlayLeg[];
    note: string;
};

const ParlayCard = () => {
    const [parlay, setParlay] = useState<ParlayRecommendation | null>(null);

    const fetchParlay = async () => {
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const res = await fetch(`${apiUrl}/ev/parlay?target_book=FanDuel&min_odds=20`);
            if (res.ok) {
                const data = await res.json();
                setParlay(data);
            }
        } catch (e) {
            console.error(e);
        }
    };

    useEffect(() => {
        fetchParlay();
    }, []);

    if (!parlay) return null;

    return (
        <div className="mb-8 p-6 bg-gradient-to-r from-blue-900 to-indigo-900 rounded-xl border border-blue-500 shadow-2xl relative overflow-hidden">
            <div className="relative z-10">
                <div className="flex justify-between items-start mb-4">
                    <div>
                        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                            <span className="text-yellow-400">⚡</span>
                            {parlay.book} 20x Value Ticket
                        </h2>
                        <p className="text-blue-200 text-sm mt-1">{parlay.note}</p>
                    </div>
                    <div className="text-right">
                        <div className="text-3xl font-black text-yellow-400">+{parlay.total_odds_american}</div>
                        <div className="text-xs text-blue-300">Total Odds</div>
                    </div>
                </div>

                <div className="space-y-3">
                    {parlay.legs.map((leg, idx) => (
                        <div key={idx} className="flex items-center justify-between bg-black/20 p-3 rounded hover:bg-black/30 transition">
                            <div>
                                <div className="font-bold text-white">{leg.selection}</div>
                                <div className="text-xs text-gray-300">{leg.match_name} ({leg.market})</div>
                            </div>
                            <div className="text-right">
                                <span className="font-mono text-green-300 font-bold">{leg.odds_american > 0 ? `+${leg.odds_american}` : leg.odds_american}</span>
                                <span className="ml-2 text-[10px] bg-green-900 text-green-200 px-1 rounded">+{leg.ev_percent.toFixed(1)}% EV</span>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="mt-6 flex justify-between items-center border-t border-blue-700/50 pt-4">
                    <div className="text-sm text-blue-200">
                        Based on mathematical edges, not "hunches".
                    </div>
                    <button onClick={fetchParlay} className="text-xs text-blue-400 hover:text-white underline">
                        Refresh Ticket
                    </button>
                </div>
            </div>

            {/* Background decoration */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500 opacity-10 rounded-full blur-3xl -mr-32 -mt-32"></div>
        </div>
    );
};

export default ParlayCard;
