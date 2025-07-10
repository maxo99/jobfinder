
import pytest

from jobfinder.utils.loader import load_data2


@pytest.fixture(scope="session")
def fix_elasticsearchclient():
    from jobfinder.adapters.elasticsearch_client import ElastiSearchClient
    _client = ElastiSearchClient()
    yield _client
    _client.close()
    
@pytest.fixture(scope="session")
def fix_jobs_data():
    return load_data2(state="processed")


@pytest.fixture(scope="session")
def mock_openai_client():
    from unittest.mock import MagicMock
    from jobfinder.adapters.chat_client import OpenAI
    mock_client = MagicMock(spec=OpenAI)
    mock_client.chat.completions.create.return_value = {
        "choices": [{"message": {"content": "Mocked response"}}]
    }
    
    yield mock_client
