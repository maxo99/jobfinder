import logging
from datetime import date
from enum import Enum
from typing import Self
import pandas as pd
from pydantic import BaseModel, Field, field_validator

from jobfinder.utils import get_now

logger = logging.getLogger(__name__)


class Status(Enum):
    NEW = "new"
    VIEWED = "viewed"
    EXCLUDED = "excluded"
    APPLIED = "applied"

class UserType(Enum):
    USER = "👤 (User)"
    AI = "🤖 (AI)"
    NA = "➖ (N/A)"



STATUS_OPTIONS = [s.value for s in Status]
DEFAULT_STATUS_FILTERS = [s.value for s in Status if s != Status.EXCLUDED]

class DataFilters(BaseModel):
    status_filters: list[str] = DEFAULT_STATUS_FILTERS
    title_filters: list[str] = []

class _FoundJob(BaseModel):
    listing_type: str | None = None
    emails: str | None = None
    company_addresses: str | None = None
    company_num_employees: str | None = None
    company_revenue: str | None = None
    company_description: str | None = None
    skills: str | None = None
    company_rating: str | None = None
    company_reviews_count: str | None = None
    vacancy_count: str | None = None
    work_from_home_type: str | None = None


class FoundJob(_FoundJob):
    # model_config = ConfigDict(extra='allow')
    id: str | None = None
    site: str | None = None
    job_url: str | None = None
    job_url_direct: str | None = None
    title: str | None = None
    company: str | None = None
    date_posted: str | None = None
    description: str | None = ""
    #
    location: str | None = None
    is_remote: bool | None = None
    #
    # Custom fields
    status: Status = Status.NEW
    classifier: UserType | None = None
    summarizer: UserType | None = None
    pros: str | None = None
    cons: str | None = None
    score: float | None = Field(default=None, json_schema_extra=dict(min=0.0, max=10.0))
    summary: str | None = None
    date_scraped: str | None = None
    modified: str | None = None
    #
    #
    #
    job_type: str | None = None
    salary_source: str | None = None
    interval: str | None = None
    min_amount: float | None = None
    max_amount: float | None = None
    currency: str | None = None
    #
    company_industry: str | None = None
    company_url: str | None = None
    company_logo: str | None = None
    company_url_direct: str | None = None
    #
    experience_range: str | None = None
    job_level: str | None = None
    job_function: str | None = None
    #

    def __str__(self) -> str:
        return f"FoundJob(ID: {self.id}, Name: {self.name})"

    @property
    def name(self) -> str:
        return f"{self.company}: {self.title}"

    @property
    def salary(self) -> str:
        return f"{self.min_amount} - {self.max_amount} {self.currency}"

    @field_validator("*", mode="before")
    @classmethod
    def allow_none(cls, v):
        if v is None or pd.isna(v):
            return None
        else:
            return v

    # @field_validator('status', mode='after')
    # def validate_status(cls, s):
    #     if s is None or pd.isna(s):
    #         return Status.NEW
    #     else:
    #         return Status(s)

    @field_validator("status", mode="after")
    @classmethod
    def validate_status(cls, s):
        if s is None or pd.isna(s):
            return Status.NEW
        else:
            return Status(s)

    @field_validator("date_posted", mode="after")
    @classmethod
    def validate_date_posted(cls, s):
        if s is None or pd.isna(s):
            return "N/A"
        elif isinstance(s, date):
            return s.strftime("%Y-%m-%d")
        return s

    @field_validator("classifier", "summarizer", mode="after")
    @classmethod
    def validate_usertype(cls, c):
        if c is None or pd.isna(c):
            return UserType.NA
        else:
            return UserType(c)

    # @field_validator('score')
    # def validate_score(cls, s):
    #     if s is None or pd.isna(s):
    #         return 5.0
    #     else:
    #         return s

    @classmethod
    def from_dict(cls, data: dict) -> Self | None:
        try:
            return cls.model_validate(data)
        except Exception as e:
            logger.error(f"Failed to convert data e:{e}")
            return cls.model_validate(
                dict(
                    id=data.get("id"),
                    site=data.get("site"),
                    job_url=data.get("job_url"),
                    job_url_direct=data.get("job_url_direct"),
                    title=data.get("title"),
                    company=data.get("company"),
                    date_posted=data.get("date_posted"),
                )
            )

    def get_details(self, long: bool = True) -> str:
        _d = [
            f"## 📝 **{self.name}**",
            f"**Company:** {self.company}",
            f"**Location:** {self.location or 'N/A'}",
            f"**Date Posted:** {self.date_posted or 'N/A'}",
            f"**Job Type:** {self.job_type or 'N/A'}",
            f"**Salary:** {self.salary or 'N/A'}",
        ]
        if self.job_url:
            _d.append(f"**{self.site} URL:** [ Job]({self.job_url})")
        if self.job_url_direct:
            _d.append(f"**{self.company} URL:** [{self.title}]({self.job_url_direct})")
        if self.description:
            _d.append("## **Description:** ")
            if long:
                _d.append(self.description)

            else:
                _d.append(
                    self.description[:1000] + "..."
                    if len(self.description) > 1000
                    else self.description
                )
        return "  \n  ".join(_d)


def found_jobs_from_df(df: pd.DataFrame) -> dict[int, FoundJob]:
    """Convert a DataFrame to a list of FoundJob instances."""
    jobs = dict()
    for i, row in df.iterrows():
        job = FoundJob.from_dict(row.to_dict())
        if job:
            jobs[i] = job
    return jobs


def validate_defaults(df):
    if "date_scraped" not in df.columns:
        df["date_scraped"] = get_now()
    if "modified" not in df.columns:
        df["modified"] = get_now()
    if "status" not in df.columns:
        df["status"] = Status.NEW.value
    if "pros" not in df.columns:
        df["pros"] = ""
    df['pros'] = df['pros'].astype(str)  # Ensure pros is string type
    if "cons" not in df.columns:
        df["cons"] = ""
    df['cons'] = df['cons'].astype(str)  # Ensure cons is string type
    if "score" not in df.columns:
        df["score"] = None
    if "summary" not in df.columns:
        df["summary"] = None
    df['summary'] = df['summary'].astype(str)  # Ensure summary is string type
    if "classifier" not in df.columns:
        df["classifier"] = UserType.NA.value
    if "summarizer" not in df.columns:
        df["summarizer"] = UserType.NA.value
    df["date_posted"] = df["date_posted"].astype(str)
