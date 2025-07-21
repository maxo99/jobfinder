# import json
# import time

# from jobfinder.services import data_service


# def test_connection(fix_elasticsearchclient):
#     try:
#         assert fix_elasticsearchclient.client.ping()
#     except Exception as e:
#         fix_elasticsearchclient.client.info()
#         print("Elasticsearch connection failed:", e)
#         raise e


# def test_create_index(fix_elasticsearchclient, test_index):
#     assert fix_elasticsearchclient.client.indices.exists(index=test_index), (
#         "Index 'jobfinder_test' should exist after creation."
#     )


# def test_populate_index(jobs_data_f, fix_elasticsearchclient, test_index):
#     test_data = jobs_data_f.copy().head(3)
#     for doc in test_data.apply(lambda x: x.to_dict(), axis=1):
#         fix_elasticsearchclient.index_document(
#             index_name=test_index, document=json.dumps(doc)
#         )
#     time.sleep(2)
#     response = fix_elasticsearchclient.client.count(index=test_index)
#     print(f"Indexed {response['count']} documents in index '{test_index}'.")
#     assert response["count"] == len(test_data), (
#         "Not all documents were indexed correctly."
#     )


# def test_title_search(jobs_data_f, fix_elasticsearchclient, test_index):
#     test_data = jobs_data_f.copy().head(3)
#     _kw = test_data["title"].iloc[0]
#     data_service.store_jobs(fix_elasticsearchclient, test_data, index_name=test_index)
#     time.sleep(2)
#     response = data_service.search_jobs_by_title(
#         search_client=fix_elasticsearchclient, keyword=_kw, index_name=test_index
#     )
#     assert len(response) > 0, (
#         f"No documents found for keyword '{_kw}' in index '{test_index}'."
#     )


# def test_update_by_id(jobs_data_f, fix_elasticsearchclient, test_index):
#     doc_df = jobs_data_f.copy().head(1)
#     doc_id = doc_df["id"].iloc[0]
#     data_service.store_jobs(fix_elasticsearchclient, doc_df, index_name=test_index)
#     new_data = {"title": "Updated Title", "description": "Updated Description"}

#     response = data_service.update_by_id(
#         search_client=fix_elasticsearchclient,
#         index_name=test_index,
#         doc_id=doc_id,
#         new_data=new_data,
#     )

#     assert response is not None, (
#         f"Failed to update document with ID '{doc_id}' in index '{test_index}'."
#     )

#     updated_doc = data_service.get_by_id(
#         search_client=fix_elasticsearchclient, index_name=test_index, doc_id=doc_id
#     )
#     assert updated_doc is not None, (
#         f"Document with ID '{doc_id}' not found after update."
#     )
#     assert updated_doc["id"] == doc_id, "Document ID does not match after update."

#     assert updated_doc["title"] == new_data["title"], (
#         "Document title was not updated correctly."
#     )
#     assert updated_doc["description"] == new_data["description"], (
#         "Document description was not updated correctly."
#     )
