import json

import httpx

from app.aiclient.intent_prompt_builder import build_programming_language_help

GEMMA_API_URL = "http://localhost:11434/api/generate"

async def respond_programming_help(language: str) -> str:
    user_input = f"Please provide key concepts and basics of {language} programming."
    prompt = build_programming_language_help(user_input)

    async with httpx.AsyncClient(timeout=60) as client:
        payload = {
            "model": "gemma3:1b",
            "prompt": prompt,
            "max_tokens": 512,
            "stream": False
        }
        response = await client.post(GEMMA_API_URL, json=payload)
        response.raise_for_status()
        response_json = response.json()

    raw_text = response_json.get("response", "").strip()

    # Strip markdown if any
    if raw_text.startswith("```json"):
        raw_text = raw_text[len("```json"):].strip()
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3].strip()

    try:
        data = json.loads(raw_text)
        return data.get("programmingHelp", "Sorry, no programming help available.")
    except json.JSONDecodeError:
        # If the model response is not valid JSON, fallback to raw text
        return raw_text or "Sorry, I could not get the programming help."