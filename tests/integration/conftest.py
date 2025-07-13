import json
import time
from openai.types.chat.chat_completion import ChatCompletionMessage, Choice, CompletionUsage
import pytest
import requests



@pytest.fixture(scope="session")
def at():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file("main.py", default_timeout=30).run(timeout=60)
    yield at
    print("Test session completed, cleaning up...")



# Pin the project name to avoid creating multiple stacks
@pytest.fixture(scope="session")
def docker_compose_project_name() -> str:
    return "jobfinder"

# Stop the stack before starting a new one
@pytest.fixture(scope="session")
def docker_setup():
    print("Stopping existing Docker stack...")
    return ["down -v", "up --build -d"]



def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def elasticsearch_service(docker_ip, docker_services):
    print("Waiting for Elasticsearch service to be responsive...")
    """Ensure that Elasticsearch service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("elasticsearch", 9200)
    url = "http://{}:{}".format(docker_ip, port)
    time.sleep(5)  # Wait for the service to start
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


@pytest.fixture(scope="session")
def fix_elasticsearchclient(elasticsearch_service):
    from jobfinder.adapters.elasticsearch_client import ElastiSearchClient

    _client = ElastiSearchClient()
    yield _client
    _client.close()



@pytest.fixture(scope="session")
def test_index(fix_elasticsearchclient):
    _test_index = "jobfinder_test"
    if fix_elasticsearchclient.client.indices.exists(index=_test_index):
        fix_elasticsearchclient.client.indices.delete(index=_test_index)
    _create_response = fix_elasticsearchclient.create_index(index_name=_test_index)
    print(f"Index creation response: {_create_response}")
    yield _test_index
    fix_elasticsearchclient.client.indices.delete(index=_test_index)


@pytest.fixture()
def mock_openai_client_summarizer(at, jobs_data_f,monkeypatch):
    from unittest.mock import MagicMock
    from jobfinder.adapters.chat_client import ChatClient
    from openai.types.chat.chat_completion import ChatCompletion
    
    
    def mock_completions(content: str) -> ChatCompletion:
        summaries = []
        for i, job in jobs_data_f.iterrows():
            summaries.append(
                {
                    "id": job["id"],
                    "summary": f"Mocked summary for {job['title']} at {job['company']}",
                }
            )
        return ChatCompletion(
            id="mocked_completion_id",
            created=1234567890,
            object="chat.completion",
            choices=[
                Choice(
                    index=0,
                    finish_reason="stop",
                    message=ChatCompletionMessage(
                        content=json.dumps({"summaries": summaries}),
                        role="assistant",
                    ),
                )
            ],
            model="gpt-4o-2024-05-13",
            usage=CompletionUsage(
                completion_tokens=5,
                prompt_tokens=36,
                total_tokens=41,
                completion_tokens_details=None,
            ),
        )

    # with patch('jobfinder.views.summarization_util.get_chat_client') as get_client_mock:
    mock_client = MagicMock(spec=ChatClient)
    mock_client._client = MagicMock()
    monkeypatch.setattr(mock_client, "completions", mock_completions)
    yield mock_client
    
@pytest.fixture()
def mock_get_jobs_df(at, jobs_data_f,monkeypatch):

    def _mock_get_jobs_df():
        return jobs_data_f

    def _get_test_session():
        return at.session_state

    monkeypatch.setattr("jobfinder.session.get_session", _get_test_session)
    yield