import { useState, useEffect } from 'react';
import type {AdviceLog} from '../types';

export const useGameWebSocket = (url: string) => {
    const [isConnected, setIsConnected] = useState(false);
    const [tips, setTips] = useState<AdviceLog[]>([]);
    const [rawEvents, setRawEvents] = useState<string[]>([]);

    useEffect(() => {
        const ws = new WebSocket(url);

        ws.onopen = () => setIsConnected(true);
        ws.onclose = () => setIsConnected(false);

        ws.onmessage = (event) => {
            try {
                const parsed = JSON.parse(event.data);

                switch (parsed.type) {
                    case 'NEW_TIP':
                        setTips(prevTips => [{
                            id: Math.random().toString(),
                            timestamp: parsed.data.timestamp,
                            message: parsed.data.message
                        }, ...prevTips]);
                        break;

                    case 'RAW_EVENT':
                        setRawEvents(prevEvents => [parsed.data, ...prevEvents]);
                        break;

                    default:
                        console.warn("Received unknown message type:", parsed.type);
                }
            } catch (e) {
                console.error("Error parsing JSON from websocket:", e);
            }
        };

        return () => ws.close();
    }, [url]);

    return { isConnected, tips, rawEvents };
};