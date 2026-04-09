export interface PlayerStats {
    kills: number;
    deaths: number;
    assists: number;
}

export interface Player {
    championName: String;
    level: number;
    kda: PlayerStats;
    items: string[],
    isMe?: boolean;
    gold?: number;
}

export interface GameState {
    gameTime: number;
    me: Player;
    allies: Player[];
    enemies: Player[];
}

export interface AdviceLog {
    id: string;
    timestamp: string;
    message: string
}