import httpx
import json

from app.aiclient.intent_prompt_builder import build_intent_prompt
from app.model.intent_results import parse_intent_response
from app.service.api_handlers.intent_handler_api import process_intent

GEMMA_API_URL = "http://localhost:11434/api/generate"


async def fetch_ai_response(user_message: str) -> str:
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

    # Extract the 'response' field which contains the AI output with markdown
    raw_text = response_json.get("response", "")

    # Remove markdown triple backticks if present
    if raw_text.startswith("```json"):
        raw_text = raw_text[len("```json"):].strip()
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3].strip()

    # Parse the cleaned JSON string
    try:
        intent_data = json.loads(raw_text)
    except json.JSONDecodeError:
        # fallback in case parsing fails
        intent_data = {"intent": "unknown", "parameters": None}

    # Call your intent processor
    reply = await process_intent(intent_data.get("intent", "unknown"), intent_data.get("parameters", None))

    return reply