def build_intent_prompt(user_input: str) -> str:
    system_instructions = """
You are an AI assistant. Your task is to identify the user's intent from the following options:
- greeting: User greets you (e.g., Hi, Good morning)
- casual_talk: General conversation or chit-chat
- programming_help: User needs programming help. Mandatory parameter: language
- observability_info: User asks about observability tools. Mandatory parameter: tool
- get_weather: User wants weather info. Mandatory parameters: location, time (optional)
- unknown: If the input does not match any intent above

Respond only with a JSON object with two keys: intent and parameters.
Parameters is an object with keys as parameter names and values extracted from user input or null if missing.

Example response:
{
  "intent": "programming_help",
  "parameters": {
    "language": "Python"
  }
}
"""

    prompt = f"<<SYS>>\n{system_instructions}\n<</SYS>>\nUser: {user_input}\nResponse:"
    return prompt
