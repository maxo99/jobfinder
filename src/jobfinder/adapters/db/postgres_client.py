import logging
from dataclasses import dataclass

import sqlmodel
from numpy import ndarray
from sqlalchemy import TextClause, create_engine, func, inspect, select, text
from sqlalchemy.orm import sessionmaker
from sqlmodel import cast, not_

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
                        if key.startswith("not_"):
                            # Handle "not equal" filters
                            actual_key = key[4:]  # Remove "not_" prefix
                            query = query.where(getattr(Job, actual_key) != value)
                        else:
                            # Handle regular equality filters
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

    def get_count(self, **filters) -> int:
        try:
            with self.session_maker() as session:
                query = select(func.count(cast(Job.id, sqlmodel.String)))
                if filters:
                    for key, value in filters.items():
                        if key.startswith("not_"):
                            actual_key = key[4:]
                            query = query.where(getattr(Job, actual_key) != value)
                        else:
                            query = query.where(getattr(Job, key) == value)
                result = session.execute(query).scalar_one()
                return result
        except Exception as e:
            logger.error(f"Error getting job count: {e}")
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

    def search_by_title_embeddings(
        self,
        title_embedding: list[float],
        job_exclusion_id: str | None = None,
        limit: int = 5,
        similarity_threshold: float = 0.999,
    ) -> SimilarityResponse:
        try:
            logger.info("Searching jobs by title embedding")
            embedding_sql = self._format_embedding(title_embedding)

            with self.session_maker() as session:
                dist = func.cosine_distance(Job.title_vector, embedding_sql)

                query = select(Job, dist.label("cosine_distance")).where(
                    dist < similarity_threshold
                )
                if job_exclusion_id is not None:
                    query = query.where(not_(Job.id == job_exclusion_id))
                results = session.execute(query.order_by(dist).limit(limit)).all()

                logger.info(f"Found {len(results)} jobs matching title embedding")
                return SimilarityResponse(
                    jobs=[r[0] for r in results], scores=[r[1] for r in results]
                )
        except Exception as e:
            logger.error(f"Error searching jobs by title: {e}")
            raise e

    def search_by_qualifications_embeddings(
        self,
        qe: list[float] | ndarray,
        job_exclusion_id: str | None = None,
        limit: int = 5,
        similarity_threshold: float = 0.999,
    ) -> SimilarityResponse:
        try:
            logger.info("Searching jobs by qualifications embedding")
            embedding_sql = self._format_embedding(qe)

            with self.session_maker() as session:
                dist = func.cosine_distance(Job.qualifications_vector, embedding_sql)

                results = (
                    session.query(Job, dist.label("cosine_distance"))
                    .filter(dist < similarity_threshold)
                    .order_by(dist)
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

    @staticmethod
    def _format_embedding(embedding: list[float] | ndarray) -> TextClause:
        """Format the embedding for SQL query."""
        if isinstance(embedding, ndarray):
            embedding = embedding.tolist()
        _embedding_str = ",".join([f"{float(x):.10f}" for x in embedding])
        return text(f"ARRAY[{_embedding_str}]::vector")

    # def search_by_combined_criteria(
    #     self,
    #     title_embedding: list[float] | None = None,
    #     qualifications_embedding: list[float] | None = None,
    #     title_weight: float = 0.4,
    #     qualifications_weight: float = 0.6,
    #     limit: int = 5,
    #     similarity_threshold: float = 0.7
    # ) -> list[Job]:
    #     try:
    #         logger.info("Searching jobs by combined title and qualifications embeddings")

    #         with self.session_maker() as session:
    #             query = session.query(Job)

    #             # Build distance calculation based on available embeddings
    #             distance_expressions = []

    #             if title_embedding and qualifications_embedding:
    #                 title_str = str(title_embedding).replace("[", "").replace("]", "")
    #                 qual_str = str(qualifications_embedding).replace("[", "").replace("]", "")
    #                 title_sql = text(f"ARRAY[{title_str}]::vector")
    #                 qual_sql = text(f"ARRAY[{qual_str}]::vector")

    #                 combined_distance = (
    #                     title_weight * func.cosine_distance(Job.title_vector, title_sql) +
    #                     qualifications_weight * func.cosine_distance(Job.qualifications_vector, qual_sql)
    #                 )
    #                 query = query.filter(
    #                     Job.title_vector.isnot(None),
    #                     Job.qualifications_vector.isnot(None)
    #                 )

    #             elif title_embedding:
    #                 title_str = str(title_embedding).replace("[", "").replace("]", "")
    #                 title_sql = text(f"ARRAY[{title_str}]::vector")
    #                 combined_distance = func.cosine_distance(Job.title_vector, title_sql)
    #                 query = query.filter(Job.title_vector.isnot(None))

    #             elif qualifications_embedding:
    #                 qual_str = str(qualifications_embedding).replace("[", "").replace("]", "")
    #                 qual_sql = text(f"ARRAY[{qual_str}]::vector")
    #                 combined_distance = func.cosine_distance(Job.qualifications_vector, qual_sql)
    #                 query = query.filter(Job.qualifications_vector.isnot(None))

    #             else:
    #                 raise ValueError("At least one embedding must be provided")

    #             results = (
    #                 query
    #                 .filter(combined_distance < similarity_threshold)
    #                 .order_by(combined_distance)
    #                 .limit(limit)
    #                 .all()
    #             )

    #             logger.info(f"Found {len(results)} jobs matching combined criteria")
    #             return results
    #     except Exception as e:
    #         logger.error(f"Error searching jobs by combined criteria: {e}")
    #         raise e
