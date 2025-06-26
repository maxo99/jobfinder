import os
import sys
import logging
from pathlib import Path
import streamlit as st
import pandas as pd
__version__ = "0.1.0"

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR =  PROJECT_ROOT.joinpath("data")

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
    if 'jobs_df' not in st.session_state:
        st.session_state.jobs_df = pd.DataFrame()
    if 'job_data_file' not in st.session_state:
        st.session_state.job_data_file = str(DATA_DIR.joinpath('jobs_data.csv'))
    return st.session_state

def get_jobs_df():
    return get_session().jobs_df

def get_job_data_file():
    return get_session().job_data_file

def set_jobs_df(df):
    get_session().jobs_df = df

__all__ = (
    "st",
    "PROJECT_ROOT",
    "DATA_DIR",
    "get_session",
    "get_jobs_df",
    "set_jobs_df",
    "get_job_data_file",
)