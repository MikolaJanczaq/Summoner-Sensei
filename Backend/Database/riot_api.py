import requests

from config.urls import BASE_URL


def get_champions_list():
    all_champs_response = requests.get(f"{BASE_URL}/champion.json").json()
    return all_champs_response["data"]


def get_champion_details(champion_id: str):
    champion = requests.get(f"{BASE_URL}/champion/{champion_id}.json").json()
    return champion["data"][champion_id]


def get_items_list():
    items_response = requests.get(f"{BASE_URL}/item.json").json()
    return items_response["data"]


def get_summoner_spells_list():
    response = requests.get(f"{BASE_URL}/summoner.json").json()
    return response["data"]
