import asyncio
import os

import httpx
import urllib3
from dotenv import load_dotenv
from pydantic.v1.utils import all_identical

from config.urls import LIVE_CLIENT_ENDPOINTS
from connection_manager import ws_manager
from listener.models import Player, GameState, ActivePlayer, Event
from llm_integration.llm_connect import ask_llm

# Ignore warning about insecure request (InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

game_data_endpoint = os.getenv("LIVE_CLIENT_SERVER")

async def read_endpoint_data(endpoint_key, params=None) -> dict | None:
    url = LIVE_CLIENT_ENDPOINTS.get(endpoint_key)
    if not url:
        print("Invalid endpoint key")
        return None

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"Connection error: {e}")
        return None


async def _fetch_and_parse_players(active_name: str) -> tuple[ActivePlayer, list[Player], list[Player]]:
    all_players_data = await read_endpoint_data("players")
    active_player_dict = await read_endpoint_data("active_player")

    if not all_players_data or not active_player_dict:
        return ValueError("Leauge API returned no data")

    active_player_extracted = {}
    for player in all_players_data:
        if player["riotId"] == active_name:
            active_player_extracted = player
            break
    active_player_data = {**active_player_extracted, **active_player_dict}
    active_player = ActivePlayer.model_validate(active_player_data)

    allies = []
    enemies = []

    for player in all_players_data:
        if player["riotId"] == active_player.name:
            continue

        parsed_player = Player.model_validate(player)
        if parsed_player.team == active_player.team:
            allies.append(parsed_player)
        else:
            enemies.append(parsed_player)

    return active_player, allies, enemies

async def read_start() -> GameState:
    game_state_data = await read_endpoint_data("game_stats")
    active_name = await read_endpoint_data("active_name")

    me, allies, enemies = await _fetch_and_parse_players(str(active_name))

    return GameState(
        game_time=game_state_data["gameTime"],
        me=me,
        enemies=enemies,
        allies=allies,
        last_event_id=0,
        on_going=True,
    )

async def update_players_stats(game_state: GameState):
    """Refresh stats of all players"""
    try:
        me, allies, enemies = await _fetch_and_parse_players(game_state.me.name)
        game_state.me = me
        game_state.allies = allies
        game_state.enemies = enemies
    except Exception as e:
        print(f"Error updating stats: {e}")

async def update_game_stats(game_state: GameState):
    game_state_data = await read_endpoint_data("game_stats")
    game_state.game_time = game_state_data["gameTime"]

async def update_state(game_state: GameState):
    """A facade that refreshes the entire game world"""
    try:
        await update_game_stats(game_state)
        await update_players_stats(game_state)
    except Exception as e:
        print(f"Error updating state: {e}")

def get_lane_opponents(me: ActivePlayer, enemies: list[Player]) -> list[Player]:
    """Returns a list of lane opponents"""
    if me.position in ["BOTTOM", "UTILITY"]:
        return [enemy for enemy in enemies if enemy.position in ["BOTTOM", "UTILITY"]]
    else:
        return [enemy for enemy in enemies if enemy.position == me.position]


# TODO maybe extract last_processed_event_id to some sort of parameter of Class like LeaugeEventListener.last_event_id
# also can move this function to that class
async def read_latest_events(last_processed_event_id: int) -> tuple[int, list[Event]]:
    new_events = []

    all_events = await read_endpoint_data("events")

    if not all_events:
        return last_processed_event_id, []

    all_events = all_events.get("Events", [])

    for event in reversed(all_events):
        event_id = event.get("EventID")

        if event_id <= last_processed_event_id:
            break

        try:
            parsed_event = Event.model_validate(event)
            new_events.append(parsed_event)
        except Exception as e:
            print(f"Error whilte parsing event {event_id}: {e}")

    if new_events:
        last_processed_event_id = new_events[0].id
        new_events.reverse()

    return last_processed_event_id, new_events


async def run_assistant_background_task():
    print("Waiting for game start")

    # waiting for game to launch
    game_state = None
    while game_state is None:
        try:
            game_state = await read_start()
        except Exception:
            print("Error reading game start")
            await asyncio.sleep(5)

    print("Game started")

    while game_state.on_going:
        try:
            await update_state(game_state)
            game_state.last_event_id, new_events = await read_latest_events(game_state.last_event_id)

            if new_events:
                print(f"Found {len(new_events)} new events")

                llm_response = await ask_llm(game_state, new_events)
                await ws_manager.broadcast(llm_response)

        except Exception as e:
            print(f"Error in assistant loop: {e}")

        await asyncio.sleep(5)

