

from jobfinder.adapters.elasticsearch_client import ElastiSearchClient


def test_connection():
    client = ElastiSearchClient()
    try:
        assert client.client.ping()
    except Exception as e:
        client.client.info()
        print("Elasticsearch connection failed:", e)
        raise e

def test_create_index():
    client = ElastiSearchClient()
    response = client.create_index(index_name='jobfinder_test')
    assert response.get('acknowledged', False), "Index creation failed or index already exists."
    
    
    
# def test_populate_index():
#     for doc in df.apply(lambda x: x.to_dict(), axis=1):
#         self.es_client.index(index=index_name, body=json.dumps(doc))