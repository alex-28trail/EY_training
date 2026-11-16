
import os

import ollama
from dotenv import load_dotenv


load_dotenv()

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:3b"
)


client = ollama.Client(host=OLLAMA_BASE_URL)


def generate_response(
    prompt: str,
    system_prompt: str = None
) -> str:
    """Generate a response using the local Ollama model."""

    messages = []

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    try:
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=messages
        )

        return response.message.content.strip()

    except Exception as error:
        print(f"Ollama error: {error}")
        return "Sorry, I couldn't generate a response. Please try again."


def check_model_connection() -> bool:
    """Check whether the configured Ollama model is available."""

    try:
        models = client.list()

        available_models = [
            model.model for model in models.models
        ]

        return any(
            model_name.split(":")[0] == OLLAMA_MODEL.split(":")[0]
            for model_name in available_models
        )

    except Exception as error:
        print(f"Could not connect to Ollama: {error}")
        return False
