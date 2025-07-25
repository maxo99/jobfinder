import logging
from dataclasses import dataclass

from sqlalchemy import create_engine, func, inspect, select, text
from sqlalchemy.orm import sessionmaker

from jobfinder import config
from jobfinder.domain.models import Job, SQLModel

logger = logging.getLogger(__name__)


@dataclass
class SimilarityResponse:
    jobs: list[Job]
    scores: list[float]


class PostgresClient:
    def __init__(self, db_url: str | None = None):
        try:
            logger.info("Initializing Postgres client")
            self.db_url = db_url or config.get_pg_url()
            self.engine = create_engine(self.db_url)
            self.session_maker = sessionmaker(bind=self.engine)
            self._session = self.session_maker()

            with self.engine.connect() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                conn.commit()

            self._create_tables()
        except Exception as e:
            logger.error(f"Error initializing Postgres client: {e}")
            raise e

    def _create_tables(self):
        if "job" not in inspect(self.engine).get_table_names():
            logger.info("Creating Postgres tables if they do not exist")
            SQLModel.metadata.create_all(self.engine)
            logger.info("Postgres tables created/checked successfully")
        else:
            logger.warning(
                f"SQL tables already exist: {list(SQLModel.metadata.tables.keys())}"
            )

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
                            if hasattr(job, key) and "vector" in key:
                                # Handle vector fields specifically
                                vector_value = getattr(job, key)
                                if vector_value is not None and len(vector_value) > 0:
                                    setattr(existing_job, key, vector_value)
                            else:
                                # Handle non-vector fields
                                if value is not None and value != "":
                                    setattr(existing_job, key, value)
                        updated_jobs.append(existing_job)
                    else:
                        session.add(job)
                        updated_jobs.append(job)
                session.commit()
                # Only refresh the jobs that are actually in this session
                if updated_jobs:
                    logger.info(f"Refreshing {len(updated_jobs)} jobs in session.")
                for job in updated_jobs:
                    session.refresh(job)
            logger.info(f"Upserted {len(updated_jobs)} jobs successfully.")
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

    def search_by_title(
        self, title_embedding: list[float], limit: int = 5
    ) -> list[Job]:
        try:
            logger.info("Searching jobs by title embedding")

            similarity_threshold: float = 0.7
            embedding_str: str = str(title_embedding).replace("[", "").replace("]", "")
            embedding_sql = text(f"ARRAY[{embedding_str}]::vector")

            with self.session_maker() as session:
                results = (
                    session.query(Job)
                    .filter(
                        func.cosine_distance(Job.title_vector, embedding_sql)
                        < similarity_threshold
                    )
                    .order_by(func.cosine_distance(Job.title_vector, embedding_sql))
                    .limit(limit)
                    .all()
                )
                logger.info(f"Found {len(results)} jobs matching title embedding")
                return results
        except Exception as e:
            logger.error(f"Error searching jobs by title: {e}")
            raise e

    def search_similar_jobs(
        self,
        qualifications_embedding: list[float],
        limit: int = 5,
        similarity_threshold: float = 0.1,
    ) -> SimilarityResponse:
        try:
            logger.info("Searching jobs by qualifications embedding")

            embedding_str: str = (
                str(qualifications_embedding).replace("[", "").replace("]", "")
            )
            embedding_sql = text(f"ARRAY[{embedding_str}]::vector")

            with self.session_maker() as session:
                distance_expr = func.cosine_distance(
                    Job.qualifications_vector, embedding_sql
                )

                results = (
                    session.query(Job, distance_expr.label("cosine_distance"))
                    .filter(distance_expr < similarity_threshold)
                    .order_by(distance_expr)
                    .limit(limit)
                    .all()
                )
                logger.info(
                    f"Found {len(results)} jobs matching qualifications embedding"
                )
                return SimilarityResponse(
                    jobs=[r[0] for r in results], scores=[r[1] for r in results]
                )
        except Exception as e:
            logger.error(f"Error searching jobs by qualifications: {e}")
            raise e
