import type {Player} from "../types.ts";

interface MainPlayerCardProps {
    player: Player;
}

export const MainPlayerCard = ({ player }: MainPlayerCardProps) => {
    return (
        <div className="flex flex-col items-center bg-slate-800 border-2 border-yellow-600/50 p-6 rounded-lg w-[340px] gap-4 shadow-lg shadow-yellow-900/20">

            {/* Champion Icon */}
            <div className="w-24 h-24 bg-yellow-500 text-slate-900 font-extrabold text-3xl flex items-center justify-center rounded-xl uppercase shadow-inner">
                {player.championName.substring(0, 3)}
            </div>

            {/* Champion name and level */}
            <div className="text-center">
                <h3 className="text-2xl font-bold text-slate-100">{player.championName}</h3>
                <p className="text-sm text-slate-400">Level {player.level}</p>
            </div>

            <div className="bg-slate-900 border border-slate-700 px-6 py-2 rounded-md">
        <span className="text-yellow-500 font-bold tracking-wide">
          ZŁOTO: {player.gold ?? 0}
        </span>
            </div>

            {/* KDA */}
            <div className="text-lg text-blue-400 font-semibold">
                KDA: {player.kda.kills}/{player.kda.deaths}/{player.kda.assists}
            </div>

            {/* Items section*/}
            <div className="w-full mt-2">
                <p className="text-xs text-slate-500 mb-2 uppercase tracking-wider">Your items:</p>

                <div className="flex justify-between gap-2">
                    {player.items.map((item, index) => (
                        <div
                            key={index}
                            className="w-10 h-10 bg-slate-900 border border-yellow-700/50 rounded flex items-center justify-center cursor-pointer hover:border-yellow-400 transition-colors"
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