import type {Player} from "../types.ts";
import {getDDragonChampionName} from "../utils/riot.ts";
import {useState} from "react";

interface MainPlayerCardProps {
    player: Player;
    patchVersion: string;
}

export const MainPlayerCard = ({ player, patchVersion }: MainPlayerCardProps) => {
    const [championImageError, setChampionImageError] = useState(false);

    const safeName = player.championName || "UNK";
    const apiReadyName = getDDragonChampionName(safeName);

    const championIconUrl = `https://ddragon.leagueoflegends.com/cdn/${patchVersion}/img/champion/${apiReadyName}.png`;

    return (
        <div className="flex flex-col items-center bg-slate-800 border-2 border-yellow-600/50 p-6 rounded-lg w-85 gap-4 shadow-lg shadow-yellow-900/20">

            {/* Champion Icon */}
            {championImageError ? (
                <div className="w-24 h-24 bg-yellow-600 text-slate-900 font-extrabold text-3xl flex items-center justify-center rounded-xl uppercase shadow-inner border border-yellow-500/50">
                    {safeName.substring(0, 3).toUpperCase()}
                </div>
            ) : (
                <img
                    src={championIconUrl}
                    alt={safeName}
                    className="w-24 h-24 rounded-xl border border-yellow-500/50 object-cover shadow-inner bg-slate-900"
                    onError={() => setChampionImageError(true)}
                />
            )}

            {/* Champion name and level */}
            <div className="text-center">
                <h3 className="text-2xl font-bold text-slate-100">{player.championName}</h3>
                <p className="text-sm text-slate-400">Level {player.level}</p>
            </div>

            <div className="bg-slate-900 border border-slate-700 px-6 py-2 rounded-md">
        <span className="text-yellow-500 font-bold tracking-wide">
          GOLD: {Math.floor(player.gold ?? 0)}
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
                    {player.items.map((itemId, index) => {
                        const itemIconUrl = `https://ddragon.leagueoflegends.com/cdn/${patchVersion}/img/item/${itemId}.png`;

                        return (
                            <div
                                key={index}
                                className="w-10 h-10 bg-slate-900 border border-yellow-700/50 rounded flex items-center justify-center cursor-pointer hover:border-yellow-400 transition-colors overflow-hidden"
                                title={`Item ID: ${itemId}`}
                            >
                                {itemId !== "0" && itemId !== "" && (
                                    <img
                                        src={itemIconUrl}
                                        alt={`Item ${itemId}`}
                                        className="w-full h-full object-cover"
                                    />
                                )}
                            </div>
                        )
                    })}
                </div>
            </div>

        </div>
    )
}