import logging

import pandas as pd
import streamlit as st

from jobfinder.bootstrap import Backend
from jobfinder.domain.constants import PRESET_TEMPLATES
from jobfinder.domain.models import DataFilters, Job, jobs_to_df

# from jobfinder.adapters.search.elasticsearch_client import ElastiSearchClient
from jobfinder.services.data_service import DataService
from jobfinder.services.generative_service import GenerativeService
from jobfinder.utils.loader import load_raw_jobs

logger = logging.getLogger(__name__)

# # Global variable to hold the Streamlit session state


def _init_session():
    # global _st
    # _st = st

    logger.info("Initializing session")

    if "backend" not in st.session_state:
        st.session_state.backend = Backend()

    if "saved_prompts" not in st.session_state:
        st.session_state.saved_prompts = PRESET_TEMPLATES

    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = next(
            iter(st.session_state.saved_prompts.values()), ""
        )
    if "selected_records" not in st.session_state:
        st.session_state.selected_records = []

    if "data_filters" not in st.session_state:
        st.session_state.data_filters = DataFilters()

    # if "filtered_jobs" not in st.session_state:
    #     reset_filtered_jobs_df()
    st.session_state.initialized = True


def _init_working_df():
    logger.info("Initializing working DataFrame")
    if "working_df" not in st.session_state:
        st.session_state.working_df = pd.DataFrame()

    if st.session_state.working_df.empty:
        logger.info(f"Startup DB count:{get_data_service().get_count()}")
    reload_working_df()

    if st.session_state.working_df.empty:
        logger.warning("No jobs found in the database. Loading from file.")
        raw_jobs = load_raw_jobs()
        if raw_jobs:
            get_data_service().store_jobs(raw_jobs)


def reload_working_df():
    logger.info("Reloading working DataFrame")
    # TODO: Readd DataFilters
    _jobs = get_data_service().get_jobs(
        not_status="excluded",
        # **get_data_filters().model_dump()
    )
    st.session_state.working_df = jobs_to_df(_jobs)
    logger.info(f"Working DF reloaded with {len(get_working_df())} records.")


def get_working_df() -> pd.DataFrame:
    if "working_df" not in st.session_state:
        _init_working_df()
    return st.session_state.working_df


def get_working_count() -> int:
    return len(get_working_df().index)


def get_jobs() -> list[Job]:
    return st.session_state.jobs

def set_jobs_df(df):
    get_session().jobs_df = df


def update_by_id(df: pd.DataFrame, job_id: str, new_data: dict) -> pd.DataFrame:
    df = df.copy()
    mask = df["id"] == job_id
    if mask.any():
        for k, v in new_data.items():
            if k in df.columns:
                df.loc[mask, k] = v
            else:
                logger.error(f"Column '{k}' does not exist in the DataFrame.")
        logger.info(f"Job {job_id} updated successfully!")
    else:
        logger.error(f"Job {job_id} not found.")
    return df

def get_selected_records() -> list[dict]:
    if not get_session().selected_records:
        return []

    selected_df = get_working_df()[
        get_working_df()["id"].isin(get_session().selected_records)
    ]
    return selected_df.to_dict("records")


def set_selected_data(record_ids: list[str]):
    get_session().selected_records = record_ids


def get_current_prompt() -> str:
    return get_session().current_prompt





def chat_enabled() -> bool:
    backend = get_backend()
    return backend.chat_enabled


def get_data_service() -> DataService:
    backend = get_backend()
    if not backend.data_service:
        raise ValueError("DataService is not initialized.")
    return backend.data_service


def get_generative_service() -> GenerativeService:
    backend = get_backend()
    if not backend.generative_service:
        raise ValueError("GenerativeService is not initialized.")
    return backend.generative_service


def get_session():
    return st.session_state


def get_backend() -> Backend:
    if "backend" not in get_session():
        _init_session()
    if not get_session().backend:
        raise ValueError("Backend not initialized. Call _init_session() first.")
    return get_session().backend


# def get_data_filters():
#     return get_session().data_filters


# def get_title_filters():
#     return get_data_filters().title_filters


# def set_title_filters(filters):
#     get_data_filters().title_filters = filters


# def get_status_filter():
#     return get_data_filters().status_filters


# def set_status_filter(status):
#     get_data_filters().status_filters = status


# def get_filtered_jobs_df() -> pd.DataFrame:
#     return get_session().filtered_jobs


# def set_filtered_jobs_df(df: pd.DataFrame):
#     get_session().filtered_jobs = df


# def reset_filtered_jobs_df():
#     _df = get_jobs_df().copy()
#     if not _df.empty:
#         apply_status_filters(_df)
#         apply_title_filters(_df)
#     set_filtered_jobs_df(_df)


# def apply_title_filters(_df):
#     if not _df.empty:
#         set_filtered_jobs_df(
#             _df[
#                 _df["title"].str.contains(
#                     "|".join(get_title_filters()), case=False, na=False
#                 )
#             ]
#         )


# def apply_status_filters(_df):
#     if not _df.empty:
#         set_filtered_jobs_df(_df[_df["status"].isin(get_status_filter())])


# def update_jobs_df(df: pd.DataFrame, update_cols: list | None = None):
#     if update_cols is None:
#         update_cols = _DEFAULT_UPDATE_COLS
#     get_jobs_df().loc[df.index, update_cols] = df[update_cols]

