import logging
import os
from abc import ABC, abstractmethod

from ollama import Client as Ollama

logger = logging.getLogger(__name__)


class EmbeddingClient(ABC):
    _client: ...
    model: str
    dimensions: int

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        raise NotImplementedError

    def close(self):
        try:
            if hasattr(self, "_client") and self._client:
                self._client.close()
                logger.info("Closed embedding client connection")
            else:
                logger.warning("No embedding client to close.")
        except Exception as e:
            logger.error(f"Error closing embedding client connection: {e}")


class OllamaEmbeddingClient(EmbeddingClient):
    def __init__(self, host="localhost", port=11434):
        self._client = Ollama(host=f"http://{host}:{port}")
        self.model = os.environ.get("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
        self.dimensions = int(os.environ.get("EMBEDDING_DIMENSION", 768))

    def embed(self, text: str) -> list[float]:
        try:
            logger.info(f"Performing embedding call with: {self.model}")
            response = self._client.embed(
                model=self.model, input=text, options={"dimensions": self.dimensions}
            )
            logger.debug(f"Returned embedding {response}")
            return response["embeddings"][0]
        except Exception as e:
            logger.error(f"Error during embedding: {e}")
            raise e
