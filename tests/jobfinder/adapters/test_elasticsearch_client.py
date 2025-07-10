

import json


def test_connection(fix_elasticsearchclient):
    try:
        assert fix_elasticsearchclient.client.ping()
    except Exception as e:
        fix_elasticsearchclient.client.info()
        print("Elasticsearch connection failed:", e)
        raise e

def test_create_index(fix_elasticsearchclient):
    response = fix_elasticsearchclient.create_index(index_name='jobfinder_test')
    assert response.get('acknowledged', False), "Index creation failed or index already exists."
    
    
    
def test_populate_index(fix_elasticsearchclient):
    for doc in df.apply(lambda x: x.to_dict(), axis=1):
        fix_elasticsearchclient.index(index='jobfinder_test', body=json.dumps(doc))