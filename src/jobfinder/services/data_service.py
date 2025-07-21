import logging

from jobfinder.adapters.db.postgres_client import PostgresClient
from jobfinder.adapters.embedding.embedding_client import EmbeddingClient
from jobfinder.domain.models import Job

logger = logging.getLogger(__name__)


class DataService:
    def __init__(self, db_client, embedding_client: EmbeddingClient):
        self.db_client: PostgresClient = db_client
        self.embedding_client = embedding_client
        if self.embedding_client:
            self.embeddings_enabled = True
        else:
            self.embeddings_enabled = False

    def store_jobs(self, jobs: list[Job]):
        self.db_client.upsert_jobs(jobs=jobs)
        logger.info(f"Added {len(jobs)} jobs.")

    def get_by_id(self, job_id: str) -> Job | None:
        try:
            return self.db_client.get_job_by_id(job_id)
        except Exception as e:
            logger.error(f"Error retrieving job by ID {job_id}: {e}")
            return None

    def get_jobs(self, **filters) -> list:
        return self.db_client.get_jobs(**filters)


    def get_count(self, **kwargs) -> int:
        try:
            return self.db_client.get_count(**kwargs)
        except Exception as e:
            logger.error(f"Error getting job count: {e}")
            return 0

    def delete_job(self, job_id: str):
        try:
            self.db_client.delete_job(job_id)
            logger.info(f"Deleted job with ID {job_id}.")
        except Exception as e:
            logger.error(f"Error deleting job {job_id}: {e}")
            raise e
