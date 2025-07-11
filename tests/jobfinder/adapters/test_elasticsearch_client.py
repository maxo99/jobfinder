

import json
import time


def test_connection(fix_elasticsearchclient):
    try:
        assert fix_elasticsearchclient.client.ping()
    except Exception as e:
        fix_elasticsearchclient.client.info()
        print("Elasticsearch connection failed:", e)
        raise e

def test_create_index(fix_elasticsearchclient,test_index):
    assert fix_elasticsearchclient.client.indices.exists(index=test_index), "Index 'jobfinder_test' should exist after creation."
     
    
def test_populate_index(jobs_data_f, fix_elasticsearchclient,test_index):
    test_data = jobs_data_f.copy().head(3) 
    for doc in test_data.apply(lambda x: x.to_dict(), axis=1):
        fix_elasticsearchclient.index_document(
            index_name=test_index,
            document=json.dumps(doc)
        )
    time.sleep(2)  # Wait for indexing to complete
    response = fix_elasticsearchclient.client.count(index=test_index)
    print(f"Indexed {response['count']} documents in index '{test_index}'.")
    assert response['count'] == len(test_data), "Not all documents were indexed correctly."
