# import logging
# from elasticsearch import Elasticsearch


# logger = logging.getLogger(__name__)

# JOBS_MAPPING = {}

# class ElastiSearchClient:
#     def __init__(self, host="localhost", port=9200):
#         self.client = Elasticsearch("http://{}:{}".format(host, port))

#     def create_index(self, index_name="jobfinder"):
#         """
#         Create an Elasticsearch index with the specified mapping.

#         :param index_name: Name of the index to be created.
#         :param mapping: The mapping configuration for the index.
#         :return: Response from Elasticsearch after creating the index.
#         """
#         if self.client.indices.exists(index=index_name):
#             logger.warning(f"Index '{index_name}' already exists. Skipping creation.")
#             return {
#                 "acknowledged": False,
#                 "message": f"Index '{index_name}' already exists.",
#             }
#         return self.client.indices.create(index=index_name, body=JOBS_MAPPING)

#     def index_document(self, index_name: str, document: dict, doc_id: str):
#         return self.client.index(index=index_name, id=doc_id, body=document)

#     def search_documents(self, index_name, query):
#         return self.client.search(index=index_name, body=query)

#     def delete_document(self, index_name, doc_id):
#         return self.client.delete(index=index_name, id=doc_id)

#     def delete_index(self, index_name: str) -> bool:
#         if self.client.indices.exists(index=index_name):
#             self.client.indices.delete(index=index_name)
#             return True
#         else:
#             logger.warning(f"Index '{index_name}' does not exist. Cannot delete.")
#             return False

#     def close(self):
#         self.client.transport.close()
