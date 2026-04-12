import type { AdviceLog } from '../types';

interface TipFeedProps {
    tips: AdviceLog[];
}

export const TipFeed = ({ tips }: TipFeedProps) => {
    return (
        <div className="bg-slate-900 border border-slate-700 rounded-lg shadow-inner h-80 flex flex-col overflow-hidden">
            {/* Header */}
            <div className="bg-slate-950/50 p-3 border-b border-slate-800 text-xs font-bold text-slate-400 tracking-wider">
                LIVE TIPS FEED
            </div>

            {/* Messages Container */}
            <div className="flex flex-col p-4 overflow-y-auto custom-scrollbar">

                {tips.length === 0 ? (
                    <div className="h-full flex items-center justify-center text-slate-600 font-mono text-sm">
                        Waiting for the first tip from LLM...
                    </div>
                ) :
                    tips.map((tip, index) => {
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