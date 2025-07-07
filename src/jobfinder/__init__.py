__version__ = "0.6.0"

import os
import sys
import logging
from pathlib import Path
import streamlit as st
import pandas as pd
import watchtower

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT.joinpath("data")
RAW_DATA_DIR = DATA_DIR.joinpath("raw")
JOBS_DATA_FILE = DATA_DIR.joinpath("jobs_data.csv")
if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
if not RAW_DATA_DIR.exists():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)



def _setup_logging():
    _lvl_string = os.environ.get("LOG_LEVEL", "INFO")
    _level = getattr(logging, _lvl_string)
    _log_formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)-12s]:%(message)s", datefmt="%m-%d %H:%M"
    )
    _handlers = []
    _file_handler = logging.FileHandler(DATA_DIR.joinpath("out.log"))
    _file_handler.setFormatter(_log_formatter)
    _handlers.append(_file_handler)
    _console_handler = logging.StreamHandler(sys.stdout)
    _console_handler.setFormatter(_log_formatter)
    _handlers.append(_console_handler)
    _handlers.extend(
        [_file_handler, _console_handler, watchtower.CloudWatchLogHandler()]
    )

    if os.environ.get("AWS_ACCESS_KEY_ID", "") and os.environ.get(
        "AWS_SECRET_ACCESS_KEY", ""
    ):
        # If AWS credentials are set, we can use CloudWatch logging
        _handlers.append(watchtower.CloudWatchLogHandler())

    logging.basicConfig(level=_level, handlers=_handlers)


_setup_logging()


def get_session():
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
        set_filtered_jobs_df(_df[
            _df["title"].str.contains(
                "|".join(get_title_filters()), case=False, na=False
            )
        ])


def apply_status_filters(_df):
    if not _df.empty:
        set_filtered_jobs_df(_df[_df["status"].isin(get_status_filter())])


_DEFAULT_UPDATE_COLS = [
    "status",
    "score",
    'summary'
    "pros",
    "cons",
    "classifier",
    "summarizer",
    "modified",
]


def update_jobs_df(df: pd.DataFrame, update_cols: list | None = None):
    if update_cols is None:
        update_cols = _DEFAULT_UPDATE_COLS
    st.session_state.jobs_df.loc[df.index, update_cols] = df[update_cols]





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
)
