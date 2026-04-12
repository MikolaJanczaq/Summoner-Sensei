from models.models import GameState, Event
from llm_integration.lm_studio_integration import call_lm_studio
from llm_integration.prompts import prompt_creator


async def ask_llm(
        game_state: GameState,
        new_events: list[Event]
) -> str:
    """Translates python objects into LLM events and connecting to API"""

    created_prompt = prompt_creator(game_state, new_events)

    # print("----SENDING PROMPT TO LLM-----")
    # print(created_prompt)
    # print("------------------------------")

    response = await call_lm_studio(created_prompt)

    # print("----RECEIVED ADVICE-----")
    # print(created_prompt)
    # print("------------------------------")

    return response

async def ask_llm_with_custom_prompt(prompt: str) -> str:
    """Sends already formated custom prompt directly to LLM"""
    response = await call_lm_studio(prompt)
    return response