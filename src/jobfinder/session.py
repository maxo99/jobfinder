import logging
import pandas as pd
import streamlit as st
from jobfinder.constants import PRESET_TEMPLATES
from jobfinder.utils.loader import load_data2
from jobfinder.model import DataFilters

logger = logging.getLogger(__name__)


def _init_session():
    logger.info("Initializing session")
    if "jobs_df" not in st.session_state:
        st.session_state.jobs_df = pd.DataFrame()

    if st.session_state.jobs_df.empty:
        st.session_state.jobs_df = load_data2()

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

    if "filtered_jobs" not in st.session_state:
        reset_filtered_jobs_df()




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
        set_filtered_jobs_df(
            _df[
                _df["title"].str.contains(
                    "|".join(get_title_filters()), case=False, na=False
                )
            ]
        )


def apply_status_filters(_df):
    if not _df.empty:
        set_filtered_jobs_df(_df[_df["status"].isin(get_status_filter())])


_DEFAULT_UPDATE_COLS = [
    "status",
    "score",
    "summarypros",
    "cons",
    "classifier",
    "summarizer",
    "modified",
]


def update_jobs_df(df: pd.DataFrame, update_cols: list | None = None):
    if update_cols is None:
        update_cols = _DEFAULT_UPDATE_COLS
    st.session_state.jobs_df.loc[df.index, update_cols] = df[update_cols]


def get_data_filters():
    return get_session().data_filters


def get_title_filters():
    return get_data_filters().title_filters


def set_title_filters(filters):
    get_data_filters().title_filters = filters


def get_status_filter():
    return get_data_filters().status_filters


def set_status_filter(status):
    get_data_filters().status_filters = status


def get_selected_records() -> list[dict]:
    if not st.session_state.selected_records:
        return []

    selected_df = get_jobs_df()[
        get_jobs_df()["id"].isin(st.session_state.selected_records)
    ]
    return selected_df.to_dict("records")


def set_selected_data(record_ids: list[str]):
    st.session_state.selected_records = record_ids
