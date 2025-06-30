__version__ = "0.3.0"
import os
import sys
import logging
from pathlib import Path
import streamlit as st
import pandas as pd
from jobfinder.model import DEFAULT_STATUS_FILTERS


PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT.joinpath("data")

_lvl_string = os.environ.get("LOG_LEVEL", 'DEBUG')
_level = getattr(logging, _lvl_string)
_log_formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s [%(name)-12s]:%(message)s",
    datefmt="%m-%d %H:%M"
)

_file_handler = logging.FileHandler(DATA_DIR.joinpath('out.log'))
_file_handler.setFormatter(_log_formatter)

_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setFormatter(_log_formatter)

logging.basicConfig(
    level=_level, handlers=[_file_handler, _console_handler]
)


def get_session():
    # # TODO: Remove defaults from here since they are set in main.py
    # if 'jobs_df' not in st.session_state:
    #     st.session_state.jobs_df = pd.DataFrame()
    # if 'job_data_file' not in st.session_state:
    #     st.session_state.job_data_file = str(DATA_DIR.joinpath('jobs_data.csv'))

    # # TODO: Remove defaults from here since they are set in main.py
    # if 'title_filters' not in st.session_state:
    #     st.session_state.title_filters = []
    # if 'status_filters' not in st.session_state:
    #     st.session_state.status_filters = DEFAULT_STATUS_FILTERS
    return st.session_state


def get_jobs_df() -> pd.DataFrame:
    return get_session().jobs_df


def set_jobs_df(df):
    get_session().jobs_df = df


def get_filtered_jobs_df() -> pd.DataFrame:
    return get_session().filtered_jobs


def set_filtered_jobs_df(df: pd.DataFrame):
    get_session().filtered_jobs = df


def reset_filtered_jobs_df():
    _df = get_jobs_df().copy()
    if not _df.empty:
        apply_status_filters(_df)
        apply_title_filters(_df)
    set_filtered_jobs_df(_df)


def apply_title_filters(_df):
    if not _df.empty:
        _df = _df[_df['title'].str.contains(
            '|'.join(get_title_filters()), case=False, na=False)
        ]


def apply_status_filters(_df):
    if not _df.empty:
        _df = _df[_df['status'].isin(get_status_filter())]


def update_jobs_df(
    df: pd.DataFrame,
    update_cols: list = [
        'status',
        'score',
        'pros',
        'cons',
        'classifier',
        'modified',
        ]
):
    st.session_state.jobs_df.loc[
        df.index, update_cols
    ] = df[update_cols]


def get_job_data_file():
    return get_session().job_data_file


def get_title_filters():
    return get_session().title_filters


def set_title_filters(filters):
    get_session().title_filters = filters


def get_status_filter():
    return get_session().status_filters


def set_status_filter(status):
    get_session().status_filters = status


__all__ = (
    "st",
    "PROJECT_ROOT",
    "DATA_DIR",
    "get_session",
    "get_jobs_df",
    "set_jobs_df",
    "get_job_data_file",
)
