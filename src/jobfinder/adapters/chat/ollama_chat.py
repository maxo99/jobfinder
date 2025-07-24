import json
import logging
import os
from typing import Any

from ollama import ChatResponse
from ollama import Client as Ollama

from jobfinder.adapters.chat.chat_client import ChatClient, CompletionResponse
from jobfinder.utils import get_now

logger = logging.getLogger(__name__)


class OllamaChatClient(ChatClient):
    _client: Ollama
    model: str

    def __init__(self, host="localhost", port=11434):
        self._client = Ollama(host=f"http://{host}:{port}")
        self.model = os.environ.get("OLLAMA_MODEL", "gemma3:1b")

    def _completions(self, content: str, format: dict[str, Any]) -> ChatResponse:
        try:
            logger.info(f"Performing completions call with: {self.model}")
            response = self._client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": content,
                    }
                ],
                format=format,
                stream=False,
                # options={"temperature": 0.0}
            )
            logger.info(f"Returned chat completion {json.dumps(response.model_dump(), indent=1)}")
            return response
        except Exception as e:
            raise e

    def _to_completion_response(self, response: ChatResponse) -> CompletionResponse:
        if not response.message.content:
            raise ValueError("No message in response")
        return CompletionResponse(
            id=response.created_at if response.created_at else get_now(),
            content=json.loads(response.message.content),
            prompt_tokens=response.prompt_eval_count if response.prompt_eval_count else 0,
            total_tokens=response.eval_count if response.eval_count else 0,
        )

