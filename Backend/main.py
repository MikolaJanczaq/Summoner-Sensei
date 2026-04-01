from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from connection_manager import ws_manager

app = FastAPI()

active_websockets: list[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
