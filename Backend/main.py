import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from endpoints import game, general, websocket
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(general.router, tags=["general"])
app.include_router(game.router, prefix="/game", tags=["game"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])