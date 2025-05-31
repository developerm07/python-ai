import json
from typing import Optional

import httpx
import re

from app.aiclient.intent_prompt_builder import build_programming_language_help, build_observability_prompt

GEMMA_API_URL = "http://localhost:11434/api/generate"

def is_probably_json(text: str) -> bool:
    # Quick check to prevent parsing plain text as JSON
    text = text.strip()
    return text.startswith('{') and text.endswith('}')

def chunk_and_summarize(raw_text: str, max_chars: int = 1000) -> str:
    raw_text = raw_text.strip()

    # Clean up Markdown if present
    raw_text = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text)

    if not raw_text:
        return "❌ Empty response received."

    # Try JSON parsing only if likely JSON
    if is_probably_json(raw_text):
        try:
            data = json.loads(raw_text)
            programming_help = data.get("programmingHelp", {})
            definition = programming_help.get("definition", "").strip()
            code_example = programming_help.get("codeExample", "").strip()

            if len(definition) > max_chars:
                definition = definition[:max_chars] + "..."
            if len(code_example) > max_chars:
                code_example = code_example[:max_chars] + "..."

            return f"**Definition:**\n{definition}\n\n**Code Example:**\n```java\n{code_example}\n```"
        except Exception as e:
            return f"❌ Could not parse JSON. Error: {e}\n\nRaw output:\n{raw_text}"

    # Fallback: treat as plain text and show
    return f"**Raw Response:**\n\n{raw_text}"


async def respond_programming_help(language: str) -> str:
    user_input = f"Please provide key concepts and basics of {language} programming."
    prompt = build_programming_language_help(user_input)

    try:
        async with httpx.AsyncClient(timeout=200) as client:
            payload = {
                "model": "gemma:2b",
                "prompt": prompt,
                "max_tokens": 900,
                "stream": False
            }
            response = await client.post(GEMMA_API_URL, json=payload)
            response.raise_for_status()
            response_json = response.json()
    except Exception as e:
        return f"❌ Error communicating with model: {e}"

    raw_text = response_json.get("response", "").strip()

    # Clean up markdown if wrapped in ```json
    if raw_text.startswith("```json"):
        raw_text = raw_text[len("```json"):].strip()
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3].strip()

    return chunk_and_summarize(raw_text) # <-- This is where raw_text is defined

    # Cleanup markdown wrapper if present
    if raw_text.startswith("```json"):
        raw_text = raw_text[len("```json"):].strip()
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3].strip()

    # Try parsing and summarizing
    try:
        return chunk_and_summarize(raw_text)
    except Exception as e:
        return f"Fallback to raw response:\n{raw_text}\n\nError: {e}"  # Now correctly using the defined raw_text

async def respond_observability_help(tool: Optional[str] = None) -> str:
    prompt = build_observability_prompt(tool)

    async with httpx.AsyncClient(timeout=180) as client:
        payload = {
            "model": "gemma:2b",
            "prompt": prompt,
            "max_tokens": 900,
            "stream": False
        }
        response = await client.post(GEMMA_API_URL, json=payload)
        response.raise_for_status()
        response_json = response.json()

    raw_text = response_json.get("response", "").strip()

    # Clean if it's wrapped in markdown
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```", 2)[-1].strip()

    return raw_text or "Sorry, no observability help available right now."