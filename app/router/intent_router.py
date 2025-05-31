# New file: app/service/intent_router.py
from app.service.session.session_state import clear_user_context, update_user_context, get_user_context
from app.service.api_handlers.intent_handler_api import (
    handle_greeting, handle_casual_talk,
    handle_programming_help, handle_observability_info,
    handle_get_weather, handle_unknown
)

INTENT_REQUIREMENTS = {
    "greeting": [],
    "casual_talk": [],
    "programming_help": ["language"],
    "observability_info": [],
    "get_weather": ["location"],  # 'time' optional
    "unknown": []
}

async def process_intent(intent: str, parameters: dict, user_id: str = "default_user") -> str:
    update_user_context(user_id, intent, parameters)
    context = get_user_context(user_id)
    current_params = context.get("parameters", {})

    missing = [p for p in INTENT_REQUIREMENTS.get(intent, []) if not current_params.get(p)]
    if missing:
        return f"To proceed with '{intent}', please provide: {', '.join(missing)}."

    clear_user_context(user_id)

    if intent == "greeting":
        return await handle_greeting()
    if intent == "casual_talk":
        return await handle_casual_talk()
    if intent == "programming_help":
        language= current_params.get("language")
        return await handle_programming_help(language)
    if intent == "observability_info":
        return await handle_observability_info(current_params.get("tool"))
    if intent == "get_weather":
        return await handle_get_weather(current_params.get("location"), current_params.get("time"))

    return await handle_unknown()