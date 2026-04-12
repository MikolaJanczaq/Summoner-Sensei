import asyncio

from Database.rag_search import get_champion_info_for_rag, find_best_items_for_problem
from ws_manager import ws_manager, build_ws_message, WsMessageType
from listener.api_client import read_latest_events
from models.models import GameState, Event
from listener.state_manager import read_start, update_state
from llm_integration.llm_connect import ask_llm, ask_llm_with_custom_prompt
from llm_integration.prompts import item_recommendation_prompt_creator
from state import store


async def process_assistant_tick(
        game_state: GameState,
        new_events: list[Event],
        last_shop_time: float
) -> tuple[str | None, float]:
    """
    Determines the prompt type, retrieves additional data (SQL/RAG)
    and queries the LLM.
    """
    SHOP_COOLDOWN = 180
    HIGH_GOLD_THRESHOLD = 1500

    current_time = game_state.game_time
    current_gold = game_state.me.gold

    is_shop_off_cooldown = (current_time - last_shop_time) > SHOP_COOLDOWN
    has_high_gold = current_gold >= HIGH_GOLD_THRESHOLD
    has_objective_gold = current_gold >= 800

    death_event = next(
        (e for e in new_events if e.name == "ChampionKill" and e.victim == game_state.me.name),
        None
    )
    objective_secured = any(e.name in {"DragonKill", "TurretKilled"} for e in new_events)

    shop_context, rag_query = None, None

    if death_event:
        killer_name = death_event.killer
        killer_info = get_champion_info_for_rag(killer_name)
        shop_context = f"You were just killed by {killer_name} ({killer_info}). You need a defensive item."
        rag_query = f"defensive items and survivability against {killer_info}"

    elif has_high_gold and is_shop_off_cooldown:
        shop_context = f"You have {int(current_gold)} gold. Find a safe place to recall and buy core items."
        rag_query = f"best core items and power spikes for {game_state.me.champion}"

    elif objective_secured and has_objective_gold and is_shop_off_cooldown:
        shop_context = f"Objective secured. You have {int(current_gold)} gold. Good time to reset and spend it."
        rag_query = f"strong items and components for {game_state.me.champion}"

    if shop_context and rag_query:
        print("Triggering Shop/RAG Advice...")
        suggested_items = find_best_items_for_problem(rag_query)
        prompt = item_recommendation_prompt_creator(game_state, shop_context, suggested_items)
        llm_response = await ask_llm_with_custom_prompt(prompt)

        return llm_response, current_time

    if new_events:
        print(f"Found {len(new_events)} new events, asking for tactical advice")
        llm_response = await ask_llm(game_state, new_events)

        return llm_response, last_shop_time

    return None, last_shop_time


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

    store.current_state = game_state

    last_shop_time = 0

    while game_state.on_going:
        store.current_state = game_state
        try:
            await update_state(game_state)
            game_state.last_event_id, new_events = await read_latest_events(game_state.last_event_id)

            llm_response, last_shop_time = await process_assistant_tick(
                game_state,
                new_events,
                last_shop_time
            )

            if llm_response:
                tip_data = {
                    "timestamp": f"{game_state.game_time //60}:{game_state.game_time % 60}",
                    "message": f"{llm_response}",
                }
                message_to_send = build_ws_message(WsMessageType.NEW_TIP, tip_data)
                await ws_manager.broadcast(message_to_send)

        except Exception as e:
            print(f"Error in assistant loop: {e}")

        await asyncio.sleep(20)

