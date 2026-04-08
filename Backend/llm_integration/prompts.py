from listener.state_manager import get_lane_opponents
from listener.models import GameState, Event, Item


def _format_player_info(game_state: GameState) -> str:
    return (
        f"Game time: {int(game_state.game_time // 60)} minutes.\n"
        f"You are playing {game_state.me.champion} ({game_state.me.position}). "
        f"Level: {game_state.me.level}, KDA: {game_state.me.scores.kills}/{game_state.me.scores.deaths}/{game_state.me.scores.assists}, "
        f"Gold: {int(game_state.me.gold)}.\n\n"
    )


def _format_lane_opponents(me, enemies) -> str:
    opponents = get_lane_opponents(me, enemies)
    if not opponents:
        return ""

    ignored_items = {"Stealth Ward", "Control Ward", "Health Potion", "Oracle Lens"}
    result = "Your direct lane opponent(s):\n"

    for opp in opponents:
        filtered_items = [item.name for item in opp.items if item.name not in ignored_items]
        items_str = ", ".join(filtered_items) if filtered_items else "No major items"
        result += (f"- {opp.champion} (Level {opp.level}, "
                   f"KDA: {opp.scores.kills}/{opp.scores.deaths}/{opp.scores.assists}). "
                   f"Items: {items_str}\n")
    return result + "\n"


def _format_rankings(allies, enemies) -> str:
    if not allies or not enemies:
        return ""

    sorted_allies = sorted(allies, key=lambda p: (p.scores.kills, -p.scores.deaths), reverse=True)
    sorted_enemies = sorted(enemies, key=lambda p: (p.scores.kills, -p.scores.deaths), reverse=True)

    ally_ranking = ", ".join([f"{p.champion} ({p.scores.kills}/{p.scores.deaths})" for p in sorted_allies])
    enemy_ranking = ", ".join([f"{p.champion} ({p.scores.kills}/{p.scores.deaths})" for p in sorted_enemies])

    return f"Ally Power Ranking: {ally_ranking}\nEnemy Threat Ranking: {enemy_ranking}\n\n"


def _format_events(events: list[Event]) -> str:
    if not events:
        return ""

    result = "Latest events on the map:\n"
    for event in events:
        event_dict = event.model_dump(exclude_none=True)
        clean_event_str = ", ".join([f"{k}: {v}" for k, v in event_dict.items()])
        result += f"- {clean_event_str}\n"
    return result


def prompt_creator(game_state: GameState, new_events: list[Event]) -> str:
    all_allies = game_state.allies + [game_state.me]
    ally_kills = sum(p.scores.kills for p in all_allies)
    enemy_kills = sum(p.scores.kills for p in game_state.enemies)

    prompt = _format_player_info(game_state)
    prompt += _format_lane_opponents(game_state.me, game_state.enemies)
    prompt += f"Global Score: Allies {ally_kills} - {enemy_kills} Enemies.\n"
    prompt += _format_rankings(all_allies, game_state.enemies)
    prompt += _format_events(new_events)

    prompt += (
        "\nBased on this information (especially your matchup, threat rankings, and recent events), "
        "give ONE strictly tactical and actionable advice.\n"
        "Consider your current gold and enemy items. "
        "Be very concise, maximum 2 sentences."
    )

    return prompt


def item_recommendation_prompt_creator(
        game_state: GameState,
        shop_context: str,
        suggested_items: list[tuple[str, str]],
) -> str:
    prompt = _format_player_info(game_state)
    prompt += f"SHOPPING CONTEXT: {shop_context}\n\n"

    prompt += "RECOMMENDED ITEMS FROM DATABASE (Based on current threat): \n"
    if suggested_items:
        for name, description in suggested_items:
            prompt += f"- {name}: {description}\n"
    else:
        prompt += f"- No specific items found. Relay on your general knowledge.\n"

    prompt += (
        "\nYOUR TASK: You are an expert League of Legends coach.\n"
        "Look at the player's current gold, their champion, and the recommended items above.\n"
        "Select EXACTLY ONE item from the recommended list that the player should buy (or start building) right now.\n"
        "Provide a maximum 2-sentence explanation of why this item is the best choice for the current situation."
    )

    return prompt