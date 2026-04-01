import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from connection_manager import ws_manager
from listener.client_listener import run_assistant_background_task


active_websockets: list[WebSocket] = []

# TODO change the way that listener is started
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting listening to LOL server.")
    task = asyncio.create_task(run_assistant_background_task())

    yield

    print("Closing server.")
    task.cancel()

app = FastAPI(lifespan=lifespan)



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
