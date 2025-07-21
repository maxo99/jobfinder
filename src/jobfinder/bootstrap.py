import logging

from jobfinder import config
from jobfinder.adapters.chat.chat_client import (
    ChatClient,
)
from jobfinder.adapters.db.postgres_client import PostgresClient
from jobfinder.adapters.embedding.embedding_client import (
    EmbeddingClient,
    OllamaEmbeddingClient,
)

# from jobfinder.adapters.search.elasticsearch_client import ElastiSearchClient
from jobfinder.services.data_service import DataService
from jobfinder.services.generative_service import GenerativeService

logger = logging.getLogger(__name__)


class Backend:
    # es_client: ElastiSearchClient
    _chat_client: ChatClient
    data_service: DataService
    _pg_client: PostgresClient
    _embedding_client: EmbeddingClient
    generative_service: GenerativeService

    def __init__(self, **kwargs):
        logger.info("Initializing Backend connections")
        self._setup_connections(**kwargs)

    def _setup_connections(self):
        self._init_client_adapters()
        self._init_app_services()

    def _init_client_adapters(self):
        # Initialize Postgres client
        # self.es_client = ElastiSearchClient()
        self._pg_client = PostgresClient()

        # Initialize Chat client if enabled
        self._init_chat_client()
        self._init_embedding_client()

    def _init_embedding_client(self):
        if config.EMBEDDINGS_ENABLED:
            # Initialize Embedding client
            self._embedding_client = OllamaEmbeddingClient()

    def _init_chat_client(self):
        if config.CHAT_MODE == "ollama":
            from jobfinder.adapters.chat.ollama_chat import OllamaChatClient

            self._chat_client = OllamaChatClient()
        elif config.CHAT_MODE == "openai":
            from jobfinder.adapters.chat.openai_chat import OpenAIChatClient

            self._chat_client = OpenAIChatClient()
        else:
            chat_mode = None
            logger.warning(
                f"Chat client will not be initialized. chat mode: {chat_mode}."
            )

    def _init_app_services(self):
        self.data_service = DataService(
            db_client=self._pg_client, embedding_client=self._embedding_client
        )
        self.generative_service = GenerativeService(chat_client=self._chat_client)

    def close_connections(self):
        try:
            # if self._es_client:
            #     self._es_client.close()
            #     logger.info("Closed Elasticsearch client connection")
            if self._chat_client:
                self._chat_client.close()
                logger.info("Closed Chat client connection")
            if self._embedding_client:
                self._embedding_client.close()
                logger.info("Closed Embedding client connection")
        except Exception as e:
            logger.error(f"Error closing connections: {e}")

    @property
    def chat_enabled(self) -> bool:
        return self._chat_client is not None
