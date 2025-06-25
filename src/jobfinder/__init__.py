import os
import sys
import logging
from pathlib import Path
import streamlit as st

# Initialize session state
# if 'jobs_df' not in st.session_state:
#     from pandas import DataFrame
#     st.session_state.jobs_df = DataFrame()
# if 'job_data_file' not in st.session_state:
#     st.session_state.job_data_file = 'jobs_data.csv'
    
# jobs_df = st.session_state.jobs_df

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


__all__ = (
    "st",
    PROJECT_ROOT,
    DATA_DIR,
    # "jobs_df"
)