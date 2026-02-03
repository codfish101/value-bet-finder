import React from 'react';
import { BetOpportunity } from '@/types';

interface EVTableProps {
    opportunities: BetOpportunity[];
}

const EVTable: React.FC<EVTableProps> = ({ opportunities }) => {
    if (opportunities.length === 0) {
        return (
            <div className="text-center p-8 bg-gray-800 rounded-lg">
                <p className="text-gray-400">No +EV opportunities found right now.</p>
                <p className="text-sm text-gray-500 mt-2">The market is efficient... for now.</p>
            </div>
        );
    }

    return (
        <div className="overflow-x-auto shadow-md sm:rounded-lg">
            <table className="w-full text-sm text-left text-gray-300">
                <thead className="text-xs uppercase bg-gray-700 text-gray-400">
                    <tr>
                        <th scope="col" className="px-6 py-3">Match</th>
                        <th scope="col" className="px-6 py-3">Book</th>
                        <th scope="col" className="px-6 py-3">Odds (Am/Dec)</th>
                        <th scope="col" className="px-6 py-3">No-Vig Prob</th>
                        <th scope="col" className="px-6 py-3 text-green-400">EV %</th>
                        <th scope="col" className="px-6 py-3">Kelly Stake ($1k)</th>
                    </tr>
                </thead>
                <tbody>
                    {opportunities.map((bet, idx) => (
                        <tr key={idx} className="bg-gray-800 border-b border-gray-700 hover:bg-gray-750">
                            <td className="px-6 py-4 font-medium text-white whitespace-nowrap">
                                {bet.match_name} <br />
                                <span className="text-xs text-gray-500">{bet.sport} - {bet.market}</span>
                            </td>
                            <td className="px-6 py-4">
                                <span className="bg-blue-900 text-blue-300 text-xs font-medium px-2.5 py-0.5 rounded">
                                    {bet.target_book}
                                </span>
                            </td>
                            <td className="px-6 py-4">
                                <span className="font-bold">{bet.target_odds_american > 0 ? `+${bet.target_odds_american}` : bet.target_odds_american}</span>
                                <span className="text-gray-500 ml-2">({bet.target_odds_decimal})</span>
                            </td>
                            <td className="px-6 py-4">
                                {(bet.fair_prob * 100).toFixed(1)}%
                            </td>
                            <td className="px-6 py-4 font-bold text-green-400">
                                +{bet.ev_percent.toFixed(2)}%
                            </td>
                            <td className="px-6 py-4">
                                <div className="flex flex-col">
                                    <span className="font-bold text-white">${bet.kelly_stake_suggested.toFixed(2)}</span>
                                    <span className="text-xs text-gray-500">{(bet.kelly_fraction * 100).toFixed(2)}% bankroll</span>
                                </div>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default EVTable;
