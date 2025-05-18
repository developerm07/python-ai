INTENT_REQUIREMENTS = {
    "greeting": [],
    "casual_talk": [],
    "programming_help": ["language"],
    "observability_info": ["tool"],
    "get_weather": ["location"],  # 'time' optional
    "unknown": []
}

async def handle_greeting():
    return ("Hello! How can I assist you today? "
            "You can ask about programming, observability tools, weather, or just have a chat.")

async def handle_casual_talk():
    return "Let's chat! What would you like to talk about?"

async def handle_programming_help(language):
    return f"I can help you with {language} programming. What specific question do you have?"

async def handle_observability_info(tool):
    return f"Here is some info about {tool}. What details are you interested in?"

async def handle_get_weather(location, time=None):
    time_str = f" at {time}" if time else ""
    return f"Fetching weather for {location}{time_str}."

async def handle_unknown():
    return ("Sorry, I didn't understand that. "
            "I can help you with programming, observability tools, weather, or casual chat.")

async def process_intent(intent: str, parameters: dict) -> str:
    missing_params = [p for p in INTENT_REQUIREMENTS.get(intent, []) if not parameters.get(p)]

    if missing_params:
        return f"Please provide the following details to continue: {', '.join(missing_params)}."

    if intent == "greeting":
        return await handle_greeting()

    if intent == "casual_talk":
        return await handle_casual_talk()

    if intent == "programming_help":
        return await handle_programming_help(parameters.get("language"))

    if intent == "observability_info":
        return await handle_observability_info(parameters.get("tool"))

    if intent == "get_weather":
        return await handle_get_weather(parameters.get("location"), parameters.get("time"))

    return await handle_unknown()