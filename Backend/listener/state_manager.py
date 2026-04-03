from listener.api_client import read_endpoint_data, _fetch_and_parse_players
from listener.models import GameState, ActivePlayer, Player


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
