from listener.models import GameState, Event


async def ask_llm(
        game_state: GameState,
        new_events: list[Event]
) -> str:
    """Translates python objects into LLM events and connecting to API"""

    context_prompt = f"Game time: {game_state.game_time // 60} minutes"
    context_prompt += (f"You play as a {game_state.me.champion} "
                       f"(KDA: {game_state.me.scores.kills}/{game_state.me.scores.deaths}/{game_state.me.scores.assists}."
                       f" You got {game_state.me.gold} gold.")

    context_prompt += "Latest events: \n"
    for event in new_events:
        context_prompt  += f"Event {event.name} Killer: {event.killer}, victim {event.victim}"

    context_prompt += "\nGiven the attention, give me ONE service and relevant tactical advice. Be concise."


    # TODO refactor this so it sends prompt to real LLM and gets an answer
    print("----SENDING PROMPT TO LLM-----")
    print(context_prompt)
    print("------------------------------")
    fake_response = (f"I noticed {len(new_events)} new events! "
                     f"Your KDA is {game_state.me.scores.kills}/{game_state.me.scores.deaths}. "
                     f"Push the wave and go back to base to spend your {game_state.me.gold} gold!")

    return fake_response