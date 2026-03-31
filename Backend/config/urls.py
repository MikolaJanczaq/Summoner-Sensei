PATCH_VERSION= "16.6.1"
BASE_URL=f"https://ddragon.leagueoflegends.com/cdn/{PATCH_VERSION}/data/en_US"

# LIVE CLIENT ENDPOINTS
# LIVE_CLIENT_ALL_DATA = "https://127.0.0.1:2999/liveclientdata/allgamedata"
#
# LIVE_CLIENT_EVENT_DATA = "https://127.0.0.1:2999/liveclientdata/eventdata"
# LIVE_CLIENT_GAME_STATS = "https://127.0.0.1:2999/liveclientdata/gamestats"
#
# LIVE_CLIENT_ACTIVE_PLAYER = "https://127.0.0.1:2999/liveclientdata/activeplayer"
# LIVE_CLIENT_ACTIVE_PLAYER_ABILITIES = "https://127.0.0.1:2999/liveclientdata/activeplayerabilities"
# LIVE_CLIENT_ACTIVE_PLAYER_STATS = "https://127.0.0.1:2999/liveclientdata/activeplayerchampionstats"
# LIVE_CLIENT_ACTIVE_PLAYER_RUNES = "https://127.0.0.1:2999/liveclientdata/activeplayerrunes"
# LIVE_CLIENT_ACTIVE_PLAYER_NAME = "https://127.0.0.1:2999/liveclientdata/activeplayername"
#
# LIVE_CLIENT_PLAYER_LIST = "https://127.0.0.1:2999/liveclientdata/playerlist"
#
# # this endpoints require additional parameter ?riotId=...
# LIVE_CLIENT_PLAYER_SCORES = "https://127.0.0.1:2999/liveclientdata/playerscores"
# LIVE_CLIENT_PLAYER_SUMMONERS = "https://127.0.0.1:2999/liveclientdata/playersummonerspells"
# LIVE_CLIENT_PLAYER_ITEMS = "https://127.0.0.1:2999/liveclientdata/playeritems"
# LIVE_CLIENT_PLAYER_MAIN_RUNES = "https://127.0.0.1:2999/liveclientdata/playermainrunes"
# LIVE_CLIENT_PLAYER_SUB_STYLE = "https://127.0.0.1:2999/liveclientdata/playersubstyle"


# OR DO IT WITH DICT???

LOCAL_HOST = "https://127.0.0.1:2999/liveclientdata"

# LIVE CLIENT ENDPOINTS
LIVE_CLIENT_ENDPOINTS = {
    "all": f"{LOCAL_HOST}/allgamedata",
    "events": f"{LOCAL_HOST}/eventdata",
    "stats": f"{LOCAL_HOST}/gamestats",
    "active_player": f"{LOCAL_HOST}/activeplayer",
    "active_abilities": f"{LOCAL_HOST}/activeplayerabilities",
    "active_stats": f"{LOCAL_HOST}/activeplayerchampionstats",
    "active_runes": f"{LOCAL_HOST}/activeplayerrunes",
    "active_name": f"{LOCAL_HOST}/activeplayername",
    "players": f"{LOCAL_HOST}/playerlist",
    # Endpoints that require additional parameter ?riotId= ...
    "p_scores": f"{LOCAL_HOST}/playerscores",
    "p_summoners": f"{LOCAL_HOST}/playersummonerspells",
    "p_items": f"{LOCAL_HOST}/playeritems",
    "p_runes": f"{LOCAL_HOST}/playermainrunes",
    "p_style": f"{LOCAL_HOST}/playersubstyle",
}




