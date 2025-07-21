import json
import logging
import os
import time
from collections.abc import Generator

import docker
import psycopg2
import pytest
import requests
from openai.types.chat.chat_completion import (
    ChatCompletion,
)
from streamlit.testing.v1 import AppTest

from jobfinder import config
from jobfinder.adapters.chat.chat_client import ChatClient
from jobfinder.adapters.db.postgres_client import PostgresClient
from jobfinder.services.data_service import DataService
from jobfinder.services.generative_service import GenerativeService

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def at():
    _at = AppTest.from_file("main.py", default_timeout=30).run(timeout=60)
    yield _at
    print("Test session completed, cleaning up...")


# Pin the project name to avoid creating multiple stacks
@pytest.fixture(scope="session")
def docker_compose_project_name() -> str:
    return "jobfinder"


@pytest.fixture(scope="session")
def docker_setup():
    """Only start Docker services if they're not already running."""
    client = docker.from_env()

    # Check if containers are already running
    try:
        if os.getenv("chat_mode", "ollama") == "ollama":
            required_containers = ["postgres", "ollama"]
        else:
            required_containers = ["postgres"]
        startup_containers = []
        for container in required_containers:
            containers = client.containers.list(filters={"name": container})
            if not any(c.status == "running" and c.health for c in containers):
                print(f"Container '{container}' is not running, adding to startup list")
                startup_containers.append(container)
            else:
                print(f"Container '{container}' is already running, skipping startup")
        if startup_containers:
            print(f"Starting containers: {', '.join(startup_containers)}")
            return ["up --build -d " + " ".join(startup_containers)]

    except Exception as e:
        print(f"Error checking container status: {e}")
        raise e


def is_responsive(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def postgres_service(docker_ip, docker_services):
    test_db = config.POSTGRES_DB + "_test"
    test_db_url = config.get_pg_url(test_db)
    conn = None
    try:
        # Connect to the admin database
        conn = psycopg2.connect(
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            dbname="postgres",
        )
        conn.autocommit = True
        cur = conn.cursor()
        # Drop test DB if exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (test_db,))
        if cur.fetchone():
            logger.info(f"Dropping existing test database: {test_db}")
            # Terminate connections to the test DB
            cur.execute(
                """
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s
            """,
                (test_db,),
            )
            cur.execute(f"DROP DATABASE IF EXISTS {test_db}")
        # Create test DB
        logger.info(f"Creating test database: {test_db}")
        cur.execute(f"CREATE DATABASE {test_db}")
        cur.close()
        conn.close()
        conn = None
        yield test_db_url
    except Exception as e:
        logger.error(f"Error provisioning test database: {e}")
        raise
    finally:
        try:
            # Drop test DB after tests
            conn = psycopg2.connect(
                user=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD,
                host=config.POSTGRES_HOST,
                port=config.POSTGRES_PORT,
                dbname="postgres",
            )
            conn.autocommit = True
            cur = conn.cursor()
            logger.info(f"Dropping test database on teardown: {test_db}")
            cur.execute(
                """
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s
            """,
                (test_db,),
            )
            cur.execute(f"DROP DATABASE IF EXISTS {test_db}")
            cur.close()
            conn.close()
        except Exception as e:
            logger.error(f"Error cleaning up test database: {e}")
            raise


@pytest.fixture(scope="session")
def ollama_service(docker_ip, docker_services):
    if config.CHAT_MODE != "ollama":
        print("Chat mode is not set to Ollama, skipping Ollama service setup.")
        return None
    print("Checking Ollama service...")

    # First check if we can connect to a local Ollama instance
    local_url = "http://127.0.0.1:11434"
    if is_responsive(local_url):
        print("Using local Ollama instance")
        return local_url
    
    # If Ollama is not running locally, we need to start it via Docker
    if not docker_services.is_service_running("ollama"):
        print("Starting Ollama service in Docker...")
        docker_services.start("ollama")
        
    # Fall back to Docker services
    print("Waiting for Docker Ollama service to be responsive...")
    port = docker_services.port_for("ollama", 11434)
    url = f"http://{docker_ip}:{port}"
    time.sleep(5)  # Wait for the service to start
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


@pytest.fixture(scope="session")
def fix_ollamachatclient(ollama_service):
    from jobfinder.adapters.chat.ollama_chat import OllamaChatClient

    _client = OllamaChatClient()
    yield _client


@pytest.fixture(scope="session")
def fix_ollamaembeddingclient(ollama_service):
    from jobfinder.adapters.embedding.embedding_client import OllamaEmbeddingClient

    _client = OllamaEmbeddingClient()
    yield _client


@pytest.fixture(scope="session")
def fix_postgresclient(postgres_service) -> Generator[PostgresClient, None, None]:
    _client = PostgresClient(postgres_service)
    yield _client
    _client.close()


# @pytest.fixture(scope="session")
# def test_index(fix_elasticsearchclient):
#     _test_index = "jobfinder_test"
#     try:
#         if fix_elasticsearchclient.client.indices.exists(index=_test_index):
#             fix_elasticsearchclient.client.indices.delete(index=_test_index)
#         _create_response = fix_elasticsearchclient.create_index(index_name=_test_index)
#         print(f"Index creation response: {_create_response}")
#         yield _test_index
#         fix_elasticsearchclient.client.indices.delete(index=_test_index)
#     except Exception as e:
#         raise e


@pytest.fixture()
def mock_openai_client_summarizer(at, jobs_data_f, monkeypatch):
    from unittest.mock import MagicMock

    def mock_completions(content: str) -> ChatCompletion:
        summaries = []
        for _, job in jobs_data_f.iterrows():
            summaries.append(
                {
                    "id": job["id"],
                    "summary": f"Mocked summary for {job['title']} at {job['company']}",
                }
            )
        return ChatCompletion.model_validate(
            {
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": json.dumps({"summaries": summaries}),
                        },
                        "finish_reason": "stop",
                    }
                ],
                "id": "mocked_completion_id",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "gpt-4o-2024-05-13",
                "usage": {
                    "completion_tokens": 5,
                    "prompt_tokens": 36,
                    "total_tokens": 41,
                    "completion_tokens_details": None,
                },
            }
        )

    # with patch('jobfinder.views.summarization_util.get_chat_client') as get_client_mock:
    mock_client = MagicMock(spec=ChatClient)
    mock_client._client = MagicMock()
    monkeypatch.setattr(mock_client, "completions", mock_completions)
    yield mock_client


@pytest.fixture()
def mock_get_jobs_df(at, jobs_data_f, monkeypatch):
    def _mock_get_jobs_df():
        return jobs_data_f

    def _get_test_session():
        return at.session_state

    monkeypatch.setattr("jobfinder.session.get_session", _get_test_session)
    yield


@pytest.fixture()
def fix_dataservice(fix_postgresclient, fix_ollamaembeddingclient) -> DataService:
    return DataService(
        db_client=fix_postgresclient,
        embedding_client=fix_ollamaembeddingclient,
    )


@pytest.fixture()
def fix_generativeservice(
    fix_ollamachatclient,
) -> Generator[GenerativeService, None, None]:
    try:
        yield GenerativeService(chat_client=fix_ollamachatclient)
    finally:
        fix_ollamachatclient.close()
