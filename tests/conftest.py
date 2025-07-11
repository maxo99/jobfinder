
import pytest

from jobfinder.utils.loader import load_data2


@pytest.fixture(scope="session")
def fix_elasticsearchclient():
    from jobfinder.adapters.elasticsearch_client import ElastiSearchClient
    _client = ElastiSearchClient()
    yield _client
    _client.close()
    
@pytest.fixture(scope="session")
def jobs_data_f():
    return load_data2(state="processed")


@pytest.fixture(scope="session")
def test_index(fix_elasticsearchclient):
    _test_index = 'jobfinder_test'
    if fix_elasticsearchclient.client.indices.exists(index=_test_index):
        fix_elasticsearchclient.client.indices.delete(index=_test_index)
    _create_response = fix_elasticsearchclient.create_index(index_name=_test_index)
    print(f"Index creation response: {_create_response}")
    yield _test_index
    fix_elasticsearchclient.client.indices.delete(index=_test_index)


@pytest.fixture(scope="session")
def mock_openai_client():
    from unittest.mock import MagicMock
    from jobfinder.adapters.chat_client import OpenAI
    mock_client = MagicMock(spec=OpenAI)
    mock_client.chat.completions.create.return_value = {
        "choices": [{"message": {"content": "Mocked response"}}]
    }
    
    yield mock_client
