import logging

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker

from jobfinder import config
from jobfinder.domain.models import Job, SQLModel

logger = logging.getLogger(__name__)


class PostgresClient:
    def __init__(self, db_url: str | None = None):
        logger.info("Initializing Postgres client")
        self.db_url = db_url or config.get_pg_url()
        self.engine = create_engine(self.db_url)
        self.session_maker = sessionmaker(bind=self.engine)
        self._session = self.session_maker()

        with self.engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()

        self._create_tables()

    def _create_tables(self):
        logger.info("Creating Postgres tables if they do not exist")
        SQLModel.metadata.create_all(self.engine)
        logger.info("Postgres tables created/checked successfully")

    def close(self):
        try:
            self._session.close()
            self.engine.dispose()
            logger.info("Closed Postgres client connection")
        except Exception as e:
            logger.error(f"Error closing Postgres client connection: {e}")
            raise e

    def upsert_job(self, job: Job):
        self.upsert_jobs([job])

    def upsert_jobs(self, jobs: list[Job]):
        try:
            logger.info(f"Upserting {len(jobs)} jobs.")
            with self.session_maker() as session:
                updated_jobs = []
                for job in jobs:
                    existing_job = session.get(Job, job.id)
                    if existing_job:
                        for key, value in job.model_dump().items():
                            if getattr(job, key):
                                setattr(existing_job, key, value)
                        updated_jobs.append(existing_job)
                    else:
                        session.add(job)
                        updated_jobs.append(job)
                session.commit()
                # Only refresh the jobs that are actually in this session
                for job in updated_jobs:
                    session.refresh(job)
        except Exception as e:
            logger.error(f"Error upserting jobs: {e}")
            raise e

    def get_jobs(self, **filters) -> list[Job]:
        try:
            logger.info(f"Fetching jobs from with {filters}")
            query = select(Job)
            with self.session_maker() as session:
                query = select(Job)
                if filters:
                    for key, value in filters.items():
                        query = query.where(getattr(Job, key) == value)
                return list(session.execute(query).scalars().all())
        except Exception as e:
            logger.error(f"Error getting jobs: {e}")
            raise e

    def get_job_by_id(self, job_id: str) -> Job | None:
        try:
            with self.session_maker() as session:
                return session.get(Job, job_id) or None
        except Exception as e:
            raise e

    def get_count(self, **kwargs) -> int:
        try:
            return len(self.get_jobs(**kwargs))
        except Exception as e:
            raise e

    def delete_job(self, job_id: str):
        try:
            with self.session_maker() as session:
                job = session.get(Job, job_id)
                if job:
                    session.delete(job)
                    session.commit()
                else:
                    raise ValueError(f"Job with id {job_id} not found")
        except Exception as e:
            raise e
