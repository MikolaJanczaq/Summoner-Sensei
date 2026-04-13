import type {Player} from "../types.ts";
import {getDDragonChampionName} from "../utils/riot.ts";
import {useState} from "react";

interface PlayerCardProps {
    player: Player;
    patchVersion: string;
}

export const PlayerCard = ({ player, patchVersion }: PlayerCardProps) => {
    const [championImageError, setChampionImageError] = useState(false);

    const safeName = player.championName || "UNK";
    const apiReadyName = getDDragonChampionName(safeName);

    const championIconUrl = `https://ddragon.leagueoflegends.com/cdn/${patchVersion}/img/champion/${apiReadyName}.png`;

    return (
        <div className="flex bg-slate-800 border border-slate-700 p-2 rounded-md w-64 gap-3 items-start shadow-sm">

            {/* Left section: Champion Icon */}
            {championImageError ? (
                <div className="w-12 h-12 shrink-0 rounded bg-yellow-600 flex items-center justify-center font-bold text-slate-900 border border-slate-500 shadow-inner">
                    {safeName.substring(0, 3).toUpperCase()}
                </div>
            ) : (
                <img
                    src={championIconUrl}
                    alt={safeName}
                    className="w-12 h-12 shrink-0 rounded bg-slate-900 border border-slate-600 object-cover"
                    onError={() => setChampionImageError(true)}
                />
            )}

            {/* Right section: Stats and items */}
            <div className="flex flex-col grow">

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
                    {player.items.map((itemId, index) => {
                        const itemIconUrl = `https://ddragon.leagueoflegends.com/cdn/${patchVersion}/img/item/${itemId}.png`;

                        return (
                            <div
                                key={index}
                                className="w-6 h-6 bg-slate-900 border border-slate-600 rounded overflow-hidden flex items-center justify-center cursor-pointer hover:border-yellow-500 transition-colors"
                            >
                                {itemId !== "0" && itemId !== "" && (
                                    <img src={itemIconUrl} alt={`Item ${itemId}`} className="w-full h-full object-cover" />
                                )}
                            </div>
                        )
                    })}
                </div>

            </div>
        </div>
    )
}