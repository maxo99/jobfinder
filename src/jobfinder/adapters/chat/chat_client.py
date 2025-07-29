import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class CompletionResponse:
    id: str
    content: dict
    prompt_tokens: int = 0
    total_tokens: int = 0


class ChatClient(ABC):
    _client: ...
    model: str

    def completions(self, content: str, format: dict[str, Any]) -> CompletionResponse:
        response = self._completions(content, format=format)
        return self._to_completion_response(response)

    @abstractmethod
    def _completions(self, content: str, format: dict[str, Any]):
        raise NotImplementedError

    @abstractmethod
    def _to_completion_response(self, response) -> CompletionResponse:
        raise NotImplementedError

    def close(self):
        try:
            if hasattr(self, "_client") and self._client:
                self._client.close()
                logger.info("Closed chat client connection")
            else:
                logger.warning("No chat client to close.")
        except Exception as e:
            logger.error(f"Error closing chat client connection: {e}")
