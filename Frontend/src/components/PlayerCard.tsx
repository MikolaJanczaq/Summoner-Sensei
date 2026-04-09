import type {Player} from "../types.ts";

interface PlayerCardProps {
    player: Player;
}

export const PlayerCard = ({ player }: PlayerCardProps) => {
    return (
        <div className="flex bg-slate-800 border border-slate-700 p-2 rounded-md w-64 gap-3 items-start shadow-sm">

            {/* Left section: Champion Icon */}
            <div className="w-12 h-12 flex-shrink-0 bg-yellow-600 text-white font-bold flex items-center justify-center rounded uppercase text-sm">
                {player.championName.substring(0, 3)}
            </div>

            {/* Right section: Stats and items */}
            <div className="flex flex-col flex-grow">

                {/* Name and level */}
                <div className="flex justify-between items-baseline">
                    <span className="font-bold text-slate-200 text-sm">{player.championName}</span>
                    <span className="text-xs text-slate-400">Lvl {player.level}</span>
                </div>

                {/* KDA */}
                <div className="text-xs text-blue-400 font-semibold mb-1">
                    KDA: {player.kda.kills}/{player.kda.deaths}/{player.kda.assists}
                </div>

                {/* Items */}
                <div className="grid grid-cols-3 gap-1">
                    {player.items.map((item, index) => (
                        <div
                            key={index}
                            className="w-6 h-6 bg-slate-900 border border-slate-600 rounded flex items-center justify-center cursor-pointer hover:border-yellow-500 transition-colors"
                            title={item}
                        >
                            {/* TODO put a real item icon here */}
                        </div>
                    ))}
                </div>

            </div>
        </div>
    )
}