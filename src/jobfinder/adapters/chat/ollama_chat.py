import logging
import os

from ollama import ChatResponse
from ollama import Client as Ollama

from jobfinder.adapters.chat.chat_client import ChatClient, CompletionResponse

logger = logging.getLogger(__name__)


class OllamaChatClient(ChatClient):
    def __init__(self, host="localhost", port=11434):
        self._client = Ollama(host=f"http://{host}:{port}")
        self.model = os.environ.get("OLLAMA_MODEL", "gemma3:1b")

    def _completions(self, content: str) -> ChatResponse:
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
                format="json",
                stream=False,
            )
            logger.debug(f"Returned chat completion {response}")
            return response
        except Exception as e:
            raise e

    def _to_completion_response(self, response: ChatResponse) -> CompletionResponse:
        return CompletionResponse(
            id=response.created_at if response.created_at else "unknown",
            content=str(response.message.content),
            prompt_tokens=response.prompt_eval_count
            if response.prompt_eval_count
            else 0,
            total_tokens=response.eval_count if response.eval_count else 0,
        )
