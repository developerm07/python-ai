from flask import Blueprint, jsonify, request

from app.service.ollama_service import OllamaService

chat_bp= Blueprint('chat', __name__)
ollama_service= OllamaService()

@chat_bp.route('/ai', methods=['POST'])
async def  ask_ai():
    data = request.json
    prompt: str = data.get("prompt", "Default prompt")
    response = await ollama_service.generate_response(prompt)
    return jsonify({"response": response})
