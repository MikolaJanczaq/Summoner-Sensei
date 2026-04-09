export const EventTicker = () => {
    const mockEvents = [
        "Dragon slayed by: blue team",
        "Tower destroyed (MID)",
        "First Blood: Zed",
        "Baron Nashor spawn in 2:30",
        "Tower destroyed (TOP)",
        "Herald slayed by: red team",
        "ACE - red team"
    ];

    return (
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-4 shadow-inner">
            <div className="text-xs font-bold text-slate-500 tracking-wider mb-3 uppercase">
                RAW EVENTS LOG
            </div>

            <div className="flex flex-wrap gap-2">
                {mockEvents.map((event, index) => (
                    <span
                        key={index}
                        className="bg-slate-800 border border-slate-600 text-slate-300 text-xs px-3 py-1.5 rounded-md hover:bg-slate-700 transition-colors cursor-default"
                    >
            {event}
          </span>
                ))}
            </div>
        </div>
    )
}