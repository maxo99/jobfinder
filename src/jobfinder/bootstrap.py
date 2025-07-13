import logging
from jobfinder.adapters.elasticsearch_client import ElastiSearchClient
from jobfinder.adapters.chat_client import ChatClient
logger = logging.getLogger(__name__)

class Backend:
    es_client: ElastiSearchClient
    chat_client: ChatClient 
    def __init__(self):
        logger.info("Initializing Backend connections")
        self._setup_connections()

    def _setup_connections(self):


        # Initialize Elasticsearch client
        self.es_client = ElastiSearchClient()

        # Initialize Chat client if enabled
        self.chat_client = ChatClient()

    def close_connections(self):
        try:
            if self.es_client:
                self.es_client.close()
                logger.info("Closed Elasticsearch client connection")
            if self.chat_client and self.chat_client._client:
                self.chat_client._client.close()
                logger.info("Closed Chat client connection")
        except Exception as e:
            logger.error(f"Error closing connections: {e}")

    @property
    def chat_enabled(self):
        """
        Check if the chat client is enabled.
        """
        return self.chat_client.ENABLED if self.chat_client else False  



    
