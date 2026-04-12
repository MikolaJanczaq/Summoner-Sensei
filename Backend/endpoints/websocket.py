from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect
from connection_manager import ws_manager

router = APIRouter()

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
