import logging
import os
import time
from collections.abc import Generator

import docker
import psycopg2
import pytest
import requests
from streamlit.testing.v1 import AppTest

from jobfinder import JOBFINDER_ROOT, PROJECT_ROOT, config
from jobfinder.adapters.db.postgres_client import PostgresClient
from jobfinder.services.data_service import DataService
from jobfinder.services.generative_service import GenerativeService

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def at():
    _at = AppTest.from_file(JOBFINDER_ROOT / "main.py", default_timeout=30).run(
        timeout=60
    )
    yield _at
    # print("Test session completed, cleaning up...")


# Pin the project name to avoid creating multiple stacks
@pytest.fixture(scope="session")
def docker_compose_project_name(keepalive, docker_compose_project_name) -> str:
    """Override `docker_compose_project_name` to make sure that we have a
    unique project name if user asked to keep containers alive. This way
    we won’t create Docker container every time we will start pytest."""

    if keepalive:
        return "jobfinder"

    return docker_compose_project_name


@pytest.fixture(scope="session")
def docker_cleanup(keepalive, docker_cleanup):
    """If user asked to keep Docker alive, make `pytest-docker` execute
    the `docker-compose version` command. This way, Docker container won’t
    be shut down."""

    if keepalive:
        return "version"

    return docker_cleanup


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


def pytest_addoption(parser):
    """Add custom options to pytest.
    Add the --keepalive option for pytest.
    """

    parser.addoption(
        "--keepalive",
        "-K",
        action="store_true",
        default=False,
        help="Keep Docker containers alive",
    )


@pytest.fixture(scope="session")
def keepalive(request):
    """Check if user asked to keep Docker running after the test."""

    return request.config.option.keepalive


# @pytest.fixture(scope='session')
# def docker_services(request, docker_compose_files, docker_ip, docker_services_project_name):
#     """Provide the docker services as a pytest fixture.

#     The services will be stopped after all tests are run.
#     """
#     keep_alive = request.config.getoption("--keepalive", False)
#     services = Services(
#         docker_compose_files,
#         docker_ip,
#         docker_services_project_name
#     )
#     yield services
#     if not keep_alive:
#         services.shutdown()


# @pytest.fixture(scope="session")
# def my_service(request):
#     if request.config.getoption("--env") == "docker":
#         request.getfixturevalue("my_container")


def is_responsive(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(PROJECT_ROOT), "docker-compose.yml")


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


# @pytest.fixture()
# def mock_openai_client_summarizer(at, jobs_data_f, monkeypatch):
#     from unittest.mock import MagicMock

#     def mock_completions(content: str) -> ChatCompletion:
#         summaries = []
#         for _, job in jobs_data_f.iterrows():
#             summaries.append(
#                 {
#                     "id": job["id"],
#                     "summary": f"Mocked summary for {job['title']} at {job['company']}",
#                 }
#             )
#         return ChatCompletion.model_validate(
#             {
#                 "choices": [
#                     {
#                         "index": 0,
#                         "message": {
#                             "role": "assistant",
#                             "content": json.dumps({"summaries": summaries}),
#                         },
#                         "finish_reason": "stop",
#                     }
#                 ],
#                 "id": "mocked_completion_id",
#                 "object": "chat.completion",
#                 "created": int(time.time()),
#                 "model": "gpt-4o-2024-05-13",
#                 "usage": {
#                     "completion_tokens": 5,
#                     "prompt_tokens": 36,
#                     "total_tokens": 41,
#                     "completion_tokens_details": None,
#                 },
#             }
#         )

#     # with patch('jobfinder.views.summarization_util.get_chat_client') as get_client_mock:
#     mock_client = MagicMock(spec=ChatClient)
#     mock_client._client = MagicMock()
#     monkeypatch.setattr(mock_client, "completions", mock_completions)
#     yield mock_client


@pytest.fixture()
def mock_get_jobs_df(at, jobs_data_f, monkeypatch):
    def _get_test_session():
        return at.session_state

    monkeypatch.setattr("jobfinder.session.get_session", _get_test_session)
    yield


@pytest.fixture(scope="session")
def fix_dataservice(fix_postgresclient, fix_ollamaembeddingclient) -> DataService:
    return DataService(
        db_client=fix_postgresclient,
        embedding_client=fix_ollamaembeddingclient,
    )


@pytest.fixture(scope="session")
def fix_generativeservice(
    fix_ollamachatclient,
) -> Generator[GenerativeService, None, None]:
    try:
        yield GenerativeService(chat_client=fix_ollamachatclient)
    finally:
        ...
        # fix_ollamachatclient.close()


@pytest.fixture(scope="session")
def fix_populated_index(fix_dataservice, jobs_testdata, fix_generativeservice):
    count = 5
    test_jobs = jobs_testdata.copy()[0:count]
    for j in test_jobs:
        j.id = f"job_{j.id}"
    logger.info(f"Testing extraction of qualifications from {count} jobs.")
    fix_generativeservice.extract_qualifications(test_jobs)

    fix_dataservice.store_jobs(test_jobs)
    time.sleep(2)
