from models.frontend_models import FrontendPlayer, KDAStats
from models.models import Player, Item


def create_frontend_player(
        raw_player: Player,
        is_me: bool = False
) -> FrontendPlayer:

    items_id = [str(item.id) for item in raw_player.items]
    current_gold = getattr(raw_player, "gold", None) if is_me else None

    return FrontendPlayer(
        championName=raw_player.champion,
        level=raw_player.level,
        kda=KDAStats(
            kills=raw_player.scores.kills,
            deaths=raw_player.scores.deaths,
            assists=raw_player.scores.assists,
        ),
        items = items_id,
        isMe = is_me,
        gold=current_gold,

    )