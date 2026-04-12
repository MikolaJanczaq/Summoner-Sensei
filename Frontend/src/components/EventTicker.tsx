interface EventTickerProps {
    events: string[];
}

export const EventTicker = ({ events }: EventTickerProps) => {
    return (
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-4 shadow-inner">
            <div className="text-xs font-bold text-slate-500 tracking-wider mb-3 uppercase">
                RAW EVENTS LOG
            </div>

            <div className="flex flex-wrap gap-2">
                {events.length === 0 ? (
                    <span className="text-slate-700 text-xs font-mono">No events detected yet...</span>
                ) : (
                events.map((event, index) => (
                    <span
                        key={index}
                        className="bg-slate-800 border border-slate-600 text-slate-300 text-xs px-3 py-1.5 rounded-md hover:bg-slate-700 transition-colors cursor-default"
                    >
                        {event}
                    </span>
                )))}
            </div>
        </div>
    )
}