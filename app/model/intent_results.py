import json
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class IntentResult:
    intent: str
    parameters: Dict[str, Optional[str]]


def parse_intent_response(raw_text: str):
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {"intent": "unknown", "parameters": None}