import logging
from typing import Self

import pandas as pd
from pgvector.sqlalchemy import Vector
from pydantic import (
    BaseModel,
    field_validator,
)
from sqlalchemy import Column, event
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel

from jobfinder.utils import get_now

logger = logging.getLogger(__name__)


def serialize_qualifications_before_flush(session: Session, flush_context, instances):
    try:
        for obj in session.new.union(session.dirty):
            if isinstance(obj, Job) and obj.qualifications:
                # Convert Qualification objects to dicts for DB storage
                if isinstance(obj.qualifications[0], Qualification):
                    obj.qualifications = [q.model_dump() for q in obj.qualifications]
    except Exception as e:
        logger.error(f"Error in before_flush serialize_qualifications: {e}")
        raise


event.listen(Session, "before_flush", serialize_qualifications_before_flush)


# Vector dimension for embeddings
EMBEDDINGS_DIMENSION = 768

NEW = "new"
VIEWED = "viewed"
EXCLUDED = "excluded"
APPLIED = "applied"
STATUS_TYPES = {NEW, VIEWED, EXCLUDED, APPLIED}
USER = "User"
AI = "AI"
NA = "N/A"
USER_TYPES = {USER, AI, NA}


DEFAULT_STATUS_FILTERS = [s for s in STATUS_TYPES if s != EXCLUDED]


class DataFilters(BaseModel):
    status_filters: list[str] = DEFAULT_STATUS_FILTERS
    title_filters: list[str] = []
    is_remote_exclusion_filter: bool = True


class Qualification(BaseModel):
    id: str = Field(description="The jobID which this qualification belongs to")
    skill: str = Field(description="The skill or technologies representing the qualification")
    experience: str = Field(description="The experience level for the skill")
    requirement: str = Field(description="Whether the skill is required, preferred, or desired")


class ScoringResponse(BaseModel):
    score: float = Field(
        default=0.0, ge=-1.0, le=1.0, description="The score of the job based on the AI analysis"
    )
    pros: str = Field(default="N/A", description="Pros of the job")
    cons: str = Field(default="N/A", description="Cons of the job")


class SummarizationResponse(BaseModel):
    summaries: list[Qualification] = Field(
        default_factory=list,
        description="List of qualifications extracted from job postings",
    )


    def get_qualifications(self, job_id: str) -> list[Qualification] | list:
        try:
            return [q for q in self.summaries if q.id == job_id]
        except Exception as e:
            logger.error(f"Error in get_qualifications: {e}")
            raise


class Job(SQLModel, table=True):
    # Primary fields
    id: str = Field(primary_key=True)
    site: str | None = None
    job_url: str | None = None
    job_url_direct: str | None = None
    title: str | None = None
    company: str | None = None
    date_posted: str | None = None
    description: str | None = ""
    location: str | None = None
    is_remote: bool | None = None

    # Status and processing fields
    status: str = Field(default="new")  # new, viewed, excluded, applied
    classifier: str | None = None  # User, AI, N/A
    summarizer: str | None = None  # User, AI, N/A

    # Analysis fields
    pros: str | None = None
    cons: str | None = None
    score: float | None = Field(default=0.0, ge=-1.0, le=1.0)
    summary: str | None = None
    qualifications: list = Field(
        default_factory=list,
        description="List of skills and requirements",
        sa_column=Column(JSONB),
    )

    # Timestamp fields
    date_scraped: str | None = None
    modified: str | None = None

    # Job details
    job_type: str | None = None
    salary_source: str | None = None
    interval: str | None = None
    min_amount: float | None = None
    max_amount: float | None = None
    currency: str | None = None

    # Company details
    company_industry: str | None = None
    company_url: str | None = None
    company_logo: str | None = None
    company_url_direct: str | None = None

    # Experience fields
    experience_range: str | None = None
    job_level: str | None = None
    job_function: str | None = None

    # Vector fields for embeddings (pgvector)
    title_vector: list[float]  | None = Field(
        default=None, sa_column=Column(Vector(EMBEDDINGS_DIMENSION))
    )
    qualifications_vector: list[float] | None = Field(
        default=None, sa_column=Column(Vector(EMBEDDINGS_DIMENSION))
    )
    summary_vector: list[float] | None = Field(
        default=None, sa_column=Column(Vector(EMBEDDINGS_DIMENSION))
    )

    def __str__(self) -> str:
        return f"Job(ID: {self.id}, Name: {self.name})"

    # @computed_field
    @property
    def name(self) -> str:
        return f"{self.company}: {self.title}"

    @property
    def salary(self) -> str:
        if self.min_amount and self.max_amount and self.currency:
            return f"{self.min_amount} - {self.max_amount} {self.currency}"
        return "N/A"

    @field_validator("*", mode="before")
    @classmethod
    def allow_none(cls, v):
        try:
            if v is None or (isinstance(v, pd.Series) and pd.isna(v).any()):
                return None
            return v
        except Exception as e:
            logger.error(f"Error in allow_none validator: {e}")
            raise

    @field_validator("status", mode="after")
    @classmethod
    def validate_status(cls, s):
        try:
            if s is None or pd.isna(s):
                return "new"
            if isinstance(s, str) and s.lower() in STATUS_TYPES:
                return s.lower()
            logger.error(f"Invalid status value: {s}, defaulting to 'new'")
            return "new"
        except Exception as e:
            logger.error(f"Error in validate_status: {e}")
            raise

    @field_validator("date_posted", mode="after")
    @classmethod
    def validate_date_posted(cls, s):
        try:
            if s is None or pd.isna(s):
                return "N/A"
            # Handle datetime objects
            if hasattr(s, "strftime"):
                return s.strftime("%Y-%m-%d")
            # Return as string if already formatted
            return str(s)
        except Exception as e:
            logger.error(f"Error in validate_date_posted: {e}")
            raise

    @field_validator("classifier", "summarizer", mode="after")
    @classmethod
    def validate_user_type(cls, c):
        try:
            if c is None or pd.isna(c):
                return "N/A"
            if isinstance(c, str) and c in USER_TYPES:
                return c
            logger.warning(f"Invalid user type value: {c}, defaulting to 'N/A'")
            return "N/A"
        except Exception as e:
            logger.error(f"Error in validate_user_type: {e}")
            raise

    @field_validator("score", mode="after")
    @classmethod
    def validate_score(cls, s):
        try:
            if s is None or pd.isna(s):
                return 0.0
            score_val = float(s)
            if -1.0 <= score_val <= 1.0:
                return score_val
            logger.error(f"Score {score_val} out of range [-1.0, 1.0], clamping")
            return max(-1.0, min(1.0, score_val))
        except Exception as e:
            logger.error(f"Error in validate_score: {e}")
            raise

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        try:
            return cls.model_validate(data)
        except Exception as e:
            logger.error(f"Failed to convert data: {e}")
            # Fallback with minimal required fields
            return cls.model_validate(
                {
                    "id": data.get("id"),
                    "site": data.get("site"),
                    "job_url": data.get("job_url"),
                    "job_url_direct": data.get("job_url_direct"),
                    "title": data.get("title"),
                    "company": data.get("company"),
                    "date_posted": data.get("date_posted"),
                }
            )

    def get_details(self, long: bool = True) -> str:
        try:
            details = [
                f"## 📝 **{self.name}**",
                f"**Company:** {self.company or 'N/A'}",
                f"**Location:** {self.location or 'N/A'}",
                f"**Date Posted:** {self.date_posted or 'N/A'}",
                f"**Job Type:** {self.job_type or 'N/A'}",
                f"**Salary:** {self.salary}",
            ]

            if self.job_url:
                details.append(f"**{self.site} URL:** [Job]({self.job_url})")
            if self.job_url_direct:
                details.append(
                    f"**{self.company} URL:** [{self.title}]({self.job_url_direct})"
                )

            return "  \n  ".join(details)
        except Exception as e:
            logger.error(f"Error generating job details: {e}")
            raise

    # @field_serializer("qualifications")
    # @classmethod
    # def serialize_qualifications(cls, val) -> list[dict]:
    #     try:
    #         if not val:
    #             return []
    #         if isinstance(val, list) and isinstance(val[0], Qualification):
    #             return [q.model_dump() for q in val]
    #         return val
    #     except Exception as e:
    #         logger.error(f"Error in serialize_qualifications: {e}")
    #         raise

    # @field_validator("qualifications", mode="before")
    # @classmethod
    # def validate_qualifications(cls, val):
    #     try:
    #         if not val:
    #             return val
    #         if isinstance(val, list) and isinstance(val[0], dict):
    #             return [Qualification(**q) for q in val]
    #         return val
    #     except Exception as e:
    #         logger.error(f"Error in validate_qualifications: {e}")
    #         raise

    # @field_validator("qualifications", mode="before")
    # @classmethod
    # def validate_qualifications(cls, val):
    #     try:
    #         if not val:
    #             return []
    #         # Convert list of Qualification objects to dicts
    #         if isinstance(val, list) and isinstance(val[0], Qualification):
    #             return [q.model_dump() for q in val]
    #         return val
    #     except Exception as e:
    #         logger.error(f"Error in validate_qualifications: {e}")
    #         raise
    def create_qualifications_text(self) -> str:
        try:
            if not self.qualifications:
                return ""

            texts = []
            for qual in self.qualifications:
                text = f"Skill: {qual.skill}, Requirement: {qual.requirement}, Experience: {qual.experience}"
                texts.append(text)

            return " | ".join(texts)
        except Exception as e:
            logger.error(f"Error creating qualifications text: {e}")
            raise

def jobs_to_df(jobs: list[Job]) -> pd.DataFrame:
    if not jobs:
        return pd.DataFrame()

    data = [{"name": job.name, **job.model_dump()} for job in jobs]
    df = pd.DataFrame(data)

    # Ensure all columns are present
    for field in Job.__fields__.keys():
        if field not in df.columns:
            df[field] = None

    return df


def df_to_jobs(df: pd.DataFrame) -> list[Job]:
    if df.empty:
        return []
    validate_df_defaults(df)
    jobs = []
    for _, row in df.iterrows():
        job_data = row.to_dict()
        job = Job.from_dict(job_data)
        jobs.append(job)

    return jobs


def validate_df_defaults(df: pd.DataFrame) -> None:
    # Ensure Proper column types
    df.loc[:, "pros"] = df["pros"].astype(str)
    df.loc[:, "cons"] = df["cons"].astype(str)
    df.loc[:, "summary"] = df["summary"].astype(str)
    df.loc[:, "date_posted"] = df["date_posted"].astype(str)
    # Set defaults
    if "date_scraped" not in df.columns:
        df["date_scraped"] = get_now()
    if "modified" not in df.columns:
        df["modified"] = get_now()
    if "status" not in df.columns:
        df["status"] = NEW
    if "pros" not in df.columns:
        df["pros"] = ""
    if "cons" not in df.columns:
        df["cons"] = ""
    if "score" not in df.columns:
        df["score"] = 0.0
    if "summary" not in df.columns:
        df["summary"] = ""
    if "classifier" not in df.columns:
        df["classifier"] = NA
    if "summarizer" not in df.columns:
        df["summarizer"] = NA
