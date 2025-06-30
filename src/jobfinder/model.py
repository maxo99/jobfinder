from enum import Enum
import pandas as pd
import logging
from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date
from typing import Optional, Self

logger = logging.getLogger(__name__)


class Status(Enum):
    NEW = "new"
    VIEWED = "viewed"
    EXCLUDED = "excluded"
    APPLIED = "applied"
# "✅""⭕"


class Classifier(Enum):
    USER = "👤 (User)"
    AI = "🤖 (AI)"
    NA = "➖ (N/A)"

STATUS_OPTIONS = [s.value for s in Status]
DEFAULT_STATUS_FILTERS = [s.value for s in Status if s != Status.EXCLUDED]

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
    date_posted: date | None = None
    description: str | None = None
    #
    location: str | None = None
    is_remote: bool | None = None
    #
    # Custom fields
    status: Status | None = None
    classifier: Classifier | None = None
    pros: str | None = None
    cons: str | None = None
    score: float | None = Field(default=None,json_schema_extra=dict(min=0.0,max=10.0))
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

    @property
    def name(self) -> str:
        return f"{self.company}: {self.title}"

    @property
    def salary(self) -> str:
        return f"{self.min_amount} - {self.max_amount} {self.currency}"

    @field_validator('*', mode='before')
    def allow_none(cls, v):
        if v is None or pd.isna(v):
            return None
        else:
            return v

    @field_validator('status', mode='after')
    def validate_status(cls, s):
        if s is None or pd.isna(s):
            return Status.NEW
        else:
            return Status(s)
    
    
    @field_validator('classifier', mode='after')
    def validate_classifier(cls, c):
        if c is None or pd.isna(c):
            return Classifier.NA
        else:
            return Classifier(c)
        
    
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
            return None

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
            _d.append(
                f"**{self.company} URL:** [{self.title}]({self.job_url_direct})")
        if self.description:
            _d.append(f"## **Description:** ")
            if long:
                _d.append(self.description)
                
            else:
                _d.append(
                    self.description[:1000] + "..."
                    if len(self.description) > 1000
                    else self.description
                )
        return "  \n  ".join(_d)


# class Compensation(BaseModel):
#     interval: Optional[CompensationInterval] = None
#     min_amount: float | None = None
#     max_amount: float | None = None
#     currency: Optional[str] = "USD"

# class JobPost(BaseModel):
#     id: str | None = None
#     title: str
#     company_name: str | None
#     job_url: str
#     job_url_direct: str | None = None
#     location: Optional[str]

#     description: str | None = None
#     company_url: str | None = None
#     company_url_direct: str | None = None

#     job_type: list[str] | None = None
#     compensation: Compensation | None = None
#     date_posted: date | None = None
#     emails: list[str] | None = None
#     is_remote: bool | None = None
#     listing_type: str | None = None

#     # LinkedIn specific
#     job_level: str | None = None

#     # LinkedIn and Indeed specific
#     company_industry: str | None = None

#     # Indeed specific
#     company_addresses: str | None = None
#     company_num_employees: str | None = None
#     company_revenue: str | None = None
#     company_description: str | None = None
#     company_logo: str | None = None
#     banner_photo_url: str | None = None

#     # LinkedIn only atm
#     job_function: str | None = None

#     # Naukri specific
#     # skills: list[str] | None = None  #from tagsAndSkills
#     # experience_range: str | None = None  #from experienceText
#     # company_rating: float | None = None  #from ambitionBoxData.AggregateRating
#     # company_reviews_count: int | None = None  #from ambitionBoxData.ReviewsCount
#     # vacancy_count: int | None = None  #from vacancy
#     # work_from_home_type: str | None = None  #from clusters.wfhType (e.g., "Hybrid", "Remote")
