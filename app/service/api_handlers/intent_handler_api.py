from app.service.api_handlers.pl_help import respond_programming_help


async def handle_greeting():
    return ("Hello! How can I assist you today? "
            "You can ask about programming, observability tools, weather, or just have a chat.")

async def handle_casual_talk():
    return "Let's chat! What would you like to talk about?"

async def handle_programming_help(language):
    return await respond_programming_help(language)
    ##return f"I can help you with {language} programming. What specific question do you have?"

async def handle_observability_info(tool):
    return f"Here is some info about {tool}. What details are you interested in?"

async def handle_get_weather(location, time=None):
    time_str = f" at {time}" if time else ""
    return f"Fetching weather for {location}{time_str}."

async def handle_unknown():
    return ("Sorry, I didn't understand that. "
            "I can help you with programming, observability tools, weather, or casual chat.")