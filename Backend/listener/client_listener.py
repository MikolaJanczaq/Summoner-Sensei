import os
import json

import requests
import urllib3
from dotenv import load_dotenv

from config.urls import LIVE_CLIENT_ENDPOINTS
from listener.models import Player, GameState, ActivePlayer

# Ignore warning about insecure request (InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

game_data_endpoint = os.getenv("LIVE_CLIENT_SERVER")

def get_client_data():
    # Using verify=False because the League of Legends client API uses a self-signed certificate
    client_response = requests.get(game_data_endpoint, verify=False)
    return client_response.json()

# Temporary loading presaved file for development purposes
with open("../data.json", "r") as f:
    presaved_json = json.load(f)

def read_endpoint_data(endpoint_key, params=None) -> dict:
    url = LIVE_CLIENT_ENDPOINTS.get(endpoint_key)
    if not url:
        print("Invalid endpoint key")
        return None

    try:
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None


def read_start():
    game_state_data = read_endpoint_data("game_state")

    all_players_data = read_endpoint_data("players")

    active_name = read_endpoint_data("active_name")
    active_player_dict = read_endpoint_data("active_player")
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
        if player["team"] == active_player.team and player["riotId"] != player.name:
            ally = Player.model_validate(player)
            allies.append(ally)
        elif player["team"] != active_player.team:
            enemy = Player.model_validate(player)
            enemies.append(enemy)

    return GameState(
        game_time=game_state_data["gameTime"],
        me=active_player,
        enemies=enemies,
        allies=allies
    )

