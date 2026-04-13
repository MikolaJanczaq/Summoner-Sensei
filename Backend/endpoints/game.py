from fastapi import APIRouter

from config.urls import PATCH_VERSION
from endpoints.mappers import create_frontend_player
from models.frontend_models import FrontendGameState
from state import store

router = APIRouter()

@router.get("/metadata")
def get_game_metadata():
    return {"status": "ok",
            "data": {
                "patchVersion": PATCH_VERSION,
                # TODO maybe implement this if we want to
                "gameMode": "CLASSIC",
                "mapName": "SummonersRift"
            }
    }

@router.get("/state")
def get_game_state():
    state = store.current_state

    if state is None:
        return {"status": "waiting",
                "message": "The game hasn't started yet"
                }

    response_data = FrontendGameState(
        gameTime=state.game_time,
        me=create_frontend_player(state.me, is_me=True),
        allies=[create_frontend_player(p) for p in state.allies],
        enemies=[create_frontend_player(p) for p in state.enemies],
    )

    return {
        "status": "in_progress",
        "data": response_data.model_dump(by_alias=True)
    }
