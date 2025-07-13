from jobfinder.domain.indexmapping import JOBS_MAPPING


class ElastiSearchClient:
    
    """
    A client for interacting with an Elasticsearch instance.
    """

    def __init__(self, host="localhost", port=9200):
        from elasticsearch import Elasticsearch

        self.client = Elasticsearch("http://{}:{}".format(host, port))


    def create_index(self, index_name='jobfinder', mapping=JOBS_MAPPING):
        """
        Create an Elasticsearch index with the specified mapping.

        :param index_name: Name of the index to be created.
        :param mapping: The mapping configuration for the index.
        :return: Response from Elasticsearch after creating the index.
        """
        if self.client.indices.exists(index=index_name):
            # If the index already exists, we can either return an error or ignore it.
            # Here we choose to ignore and return a message indicating the index already exists.
            return {"acknowledged": False, "message": f"Index '{index_name}' already exists."}
        return self.client.indices.create(index=index_name, body=mapping)

    def index_document(self, index_name, document, doc_id=None):
        """
        Index a document in the specified Elasticsearch index.

        :param index_name: Name of the index to store the document in.
        :param document: The document to be indexed.
        :param doc_id: Optional ID for the document. If not provided, Elasticsearch will generate one.
        :return: Response from Elasticsearch after indexing the document.
        """
        return self.client.index(index=index_name, id=doc_id, body=document)

    def search_documents(self, index_name, query):
        """
        Search for documents in the specified Elasticsearch index.

        :param index_name: Name of the index to search in.
        :param query: The search query as a dictionary.
        :return: Search results from Elasticsearch.
        """
        return self.client.search(index=index_name, body=query)

    def delete_document(self, index_name, doc_id):
        """
        Delete a document from the specified Elasticsearch index.

        :param index_name: Name of the index to delete from.
        :param doc_id: ID of the document to be deleted.
        :return: Response from Elasticsearch after deletion.
        """
        return self.client.delete(index=index_name, id=doc_id)

    def close(self):
        """
        Close the connection to Elasticsearch.
        """
        self.client.transport.close()
