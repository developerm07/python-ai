# Simple in-memory session store
user_session = {}

def get_user_context(user_id: str):
    return user_session.get(user_id, {"intent": None, "parameters": {}})

def update_user_context(user_id: str, intent: str, parameters: dict):
    ctx = user_session.get(user_id, {"intent": None, "parameters": {}})

    # Ensure 'parameters' is a dictionary
    if not isinstance(ctx.get("parameters"), dict):
        ctx["parameters"] = {}

    if parameters:
        ctx["parameters"].update(parameters)

    ctx["intent"] = intent
    user_session[user_id] = ctx

def clear_user_context(user_id: str):
    if user_id in user_session:
        del user_session[user_id]