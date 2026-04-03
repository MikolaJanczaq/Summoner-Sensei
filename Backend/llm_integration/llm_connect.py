from listener.models import GameState, Event
from llm_integration.lm_studio_integration import call_lm_studio


def promp_creator(game_state: GameState, new_events: list[Event]) -> str:
    context_prompt = f"Game time: {game_state.game_time // 60} minutes"
    context_prompt += (f"You play as a {game_state.me.champion} "
                       f"(KDA: {game_state.me.scores.kills}/{game_state.me.scores.deaths}/{game_state.me.scores.assists}."
                       f" You got {int(game_state.me.gold)} gold.")

    context_prompt += "Latest events on the map: \n"
    for event in new_events:
        # TODO strip dict from sign like {":( so the LLM gets only text and not waste tokens
        event_dict = event.model_dump(exclude_none=True)
        context_prompt += f"-{event_dict}"

    context_prompt += \
        "\nBased on this information, give me ONE strictly tactical and actionable advice \n"\
        "Be very concise, maximum 2 sentences."

    return context_prompt


async def ask_llm(
        game_state: GameState,
        new_events: list[Event]
) -> str:
    """Translates python objects into LLM events and connecting to API"""

    created_prompt = promp_creator(game_state, new_events)

    # print("----SENDING PROMPT TO LLM-----")
    # print(created_prompt)
    # print("------------------------------")

    response = await call_lm_studio(created_prompt)

    # print("----RECEIVED ADVICE-----")
    # print(created_prompt)
    # print("------------------------------")

    return response