import logging

from jobfinder.adapters.db.postgres_client import PostgresClient, SimilarityResponse
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

    def embed_populated_jobs(self, jobs: list[Job]):
        try:
            for job in jobs:
                if job.title:
                    job.title_vector = self.embedding_client.embed(job.title)
                if job.qualifications:
                    job.qualifications_vector = self.embedding_client.embed(
                        job.create_qualifications_text()
                    )
            self.store_jobs(jobs)
            logger.info(f"Embedded {len(jobs)} populated jobs.")
        except Exception as e:
            logger.error(f"Error embedding populated jobs: {e}")
            raise e

    def search_similar_jobs(self, title: str, **filters) -> list[Job]:
        try:
            title_vector = self.embedding_client.embed(title)
            return self.db_client.search_by_title(title_embedding=title_vector)
        except Exception as e:
            logger.error(f"Error searching jobs with title '{title}': {e}")
            return []

    def search_by_qualifications(
        self,
        job: Job,
        limit: int = 5,
        similarity_threshold: float = 0.1,
    ) -> SimilarityResponse | None:
        try:
            if not job.qualifications_vector:
                job.qualifications_vector = self.embedding_client.embed(
                    job.create_qualifications_text()
                )
            _results = self.db_client.search_similar_jobs(
                qualifications_embedding=job.qualifications_vector,
                limit=limit,
                similarity_threshold=similarity_threshold,
            )
            return _results
        except Exception as e:
            logger.error(f"Error searching jobs by qualifications: {e}")
            return None
