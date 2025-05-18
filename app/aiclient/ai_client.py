import json

import httpx

from app.aiclient.intent_prompt_builder import build_intent_prompt
from app.router.intent_router import process_intent

GEMMA_API_URL = "http://localhost:11434/api/generate"


async def fetch_ai_response(user_message: str, user_id: str = "default_user") -> str:
    prompt = build_intent_prompt(user_message)

    async with httpx.AsyncClient(timeout=30) as client:
        payload = {
            "model": "gemma3:1b",
            "prompt": prompt,
            "max_tokens": 512,
            "stream": False
        }
        response = await client.post(GEMMA_API_URL, json=payload)
        response.raise_for_status()
        response_json =  response.json()

    raw_text = response_json.get("response", "")

    # Remove markdown formatting if needed
    if raw_text.startswith("```json"):
        raw_text = raw_text[len("```json"):].strip()
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3].strip()

    try:
        intent_data = json.loads(raw_text)
    except json.JSONDecodeError:
        intent_data = {"intent": "unknown", "parameters": None}

    reply = await process_intent(intent_data.get("intent", "unknown"),
                                 intent_data.get("parameters", {}),
                                 user_id=user_id)

    return reply


