import os

import httpx
import urllib3
from dotenv import load_dotenv

from config.urls import LIVE_CLIENT_ENDPOINTS
from listener.models import ActivePlayer, Player, Event

# Ignore warning about insecure request (InsecureRequestWarning)

load_dotenv()
game_data_endpoint = os.getenv("LIVE_CLIENT_SERVER")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
