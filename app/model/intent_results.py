import json

def parse_intent_response(response_text: str) -> dict:
    """
    Parse the AI model's JSON response to extract intent and parameters.
    Returns dict like:
    {
      "intent": "programming_help",
      "parameters": {
          "language": "Python"
      }
    }
    If parsing fails, returns {"intent": "unknown", "parameters": {}}
    """
    try:
        result = json.loads(response_text)
        intent = result.get("intent", "unknown")
        parameters = result.get("parameters", {})
        if not isinstance(parameters, dict):
            parameters = {}
        return {"intent": intent, "parameters": parameters}
    except Exception:
        return {"intent": "unknown", "parameters": {}}