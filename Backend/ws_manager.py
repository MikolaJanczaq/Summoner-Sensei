import json
from enum import Enum
from typing import Any

from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accepts new connection and adds it to the list of active connections"""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New client connected! Active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Removes connection and removes it from the list"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"Client disconnected. Left connections: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        """Broadcasts message to all active connections"""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message: {e}")
                self.disconnect(connection)

# One global instance
ws_manager = ConnectionManager()

class WsMessageType(str, Enum):
    NEW_TIP = "NEW_TIP"
    STATE_UPDATE = "STATE_UPDATE"
    RAW_EVENT = "RAW_EVENT"


def build_ws_message(message_type: WsMessageType, data: dict[str, Any]) -> str:
    """Packs a data into with message type"""
    payload = {
        "type": message_type.value,
        "data": data
    }
    return json.dumps(payload)