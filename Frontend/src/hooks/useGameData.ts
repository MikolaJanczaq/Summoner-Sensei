import { useState, useEffect } from 'react';
import type {GameState, GameMetadata, AdviceLog} from '../types';

export const useGameData = (baseUrl: string, wsUrl: string) => {
    const [metadata, setMetadata] = useState<GameMetadata | null>(null);
    const [gameState, setGameState] = useState<GameState | null>(null);
    const [tips, setTips] = useState<AdviceLog[]>([]);
    const [rawEvents, setRawEvents] = useState<string[]>([]);
    const [isConnected, setIsConnected] = useState(false);

    const [isWaitingForGame, setIsWaitingForGame] = useState(true);

    useEffect(() => {
        let ws: WebSocket;

        const fetchInitialData = async () => {
            try {
                const metaRes = await fetch(`${baseUrl}/game/metadata`);
                const metaJson = await metaRes.json();

                if (metaJson.status === 'ok') {
                    setMetadata(metaJson.data);
                }

                const stateRes = await fetch(`${baseUrl}/game/state`);
                const stateJson = await stateRes.json();

                if (stateJson.status === 'in_progress') {
                    setGameState(stateJson.data);
                    setIsWaitingForGame(false);
                    connectWebSocket();
                } else {
                    setIsWaitingForGame(true);
                }
            } catch (error) {
                console.error("Server connect error:", error);
            }
        };

        const connectWebSocket = () => {
            ws = new WebSocket(wsUrl);

            ws.onopen = () => setIsConnected(true);
            ws.onclose = () => setIsConnected(false);

            ws.onmessage = (event) => {
                try {
                    const parsed = JSON.parse(event.data);

                    switch (parsed.type) {
                        case 'NEW_TIP':
                            setTips(prev => [{
                                id: Math.random().toString(),
                                timestamp: parsed.data.timestamp,
                                message: parsed.data.message
                            }, ...prev]);
                            break;

                        case 'RAW_EVENT':
                            setRawEvents(prev => [parsed.data, ...prev]);
                            break;

                        case 'STATE_UPDATE':
                            // console.log("State update!", parsed.data);
                            setGameState(parsed.data);
                            break;
                    }
                } catch (e) {
                    console.error("Błąd parsowania JSON:", e);
                }
            };
        };

        fetchInitialData();

        return () => {
            if (ws) ws.close();
        };
    }, [baseUrl, wsUrl]);

    return {
        metadata,
        gameState,
        tips,
        rawEvents,
        isConnected,
        isWaitingForGame
    };
};