from fastapi import APIRouter

from app.aiclient.ai_client import fetch_ai_response
from app.model.ai_request import AIRequest
from app.model.ai_response import AIResponse


class OllamaService:

    async def generate_response(self, prompt):
        response = await fetch_ai_response(prompt)  # this is string
        return response

