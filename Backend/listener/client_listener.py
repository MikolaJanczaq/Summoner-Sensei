import asyncio
from connection_manager import ws_manager
from listener.api_client import read_latest_events
from listener.state_manager import read_start, update_state
from llm_integration.llm_connect import ask_llm

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

