import type { AdviceLog } from '../types';

export const TipFeed = () => {
    const mockTips: AdviceLog[] = [
        { id: '1', timestamp: '[14:40]', message: 'TACTICAL ADVICE: Focus on securing drake in 30 seconds. You have a lot of gold, recall to base.' },
        { id: '2', timestamp: '[14:32]', message: 'Buy Guardian Angel. Focus on protecting the carry.' },
        { id: '3', timestamp: '[14:15]', message: 'Watch out for Rengar. His Ult is up.' },
        { id: '4', timestamp: '[14:05]', message: 'Secure the drake in 30 seconds.' },
        { id: '5', timestamp: '[13:58]', message: 'Recall and buy items.' },
        { id: '6', timestamp: '[13:45]', message: 'Push mid lane before next objective.' },
    ];

    return (
        <div className="bg-slate-900 border border-slate-700 rounded-lg shadow-inner h-80 flex flex-col overflow-hidden">
            {/* Header */}
            <div className="bg-slate-950/50 p-3 border-b border-slate-800 text-xs font-bold text-slate-400 tracking-wider">
                LIVE TIPS FEED
            </div>

            {/* Messages Container */}
            <div className="flex flex-col p-4 overflow-y-auto custom-scrollbar">
                {mockTips.map((tip, index) => {
                    const isLatest = index === 0;

                    return (
                        <div
                            key={tip.id}
                            className={`
                                mb-3 transition-all
                                ${isLatest
                                ? 'bg-slate-800 border-l-4 border-yellow-500 p-4 rounded-r-md shadow-md mt-1 mb-6'
                                : 'flex gap-3 items-start font-mono text-sm py-1 px-2 hover:bg-slate-800/50 rounded'
                            }
                            `}
                        >
                            {/* Timestamp */}
                            <span className={`font-bold flex-shrink-0 ${isLatest ? 'text-yellow-500 mr-2' : 'text-slate-500'}`}>
                                {tip.timestamp}
                            </span>

                            {/* Message content */}
                            <span className={`${isLatest ? 'text-lg text-slate-200 font-medium' : 'text-slate-400'}`}>
                                {tip.message}
                            </span>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}