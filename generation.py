import os
from typing import List, Dict

from dotenv import load_dotenv
from ollama import Client

load_dotenv()

ollama_client = Client(host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))


def generation(prompt_messages: List[Dict[str, str]]) -> str:
    # Convert the messages to Ollama format
    messages = [
        {"role": msg["role"], "content": msg["content"]} for msg in prompt_messages
    ]

    response = ollama_client.chat(
        model=os.environ.get("CHAT_COMPLETION_MODEL", "llama3.2"),
        messages=messages,
        options={"temperature": 0},
    )

    return response["message"]["content"]
