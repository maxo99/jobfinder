import logging

import streamlit as st

from jobfinder import __version__
from jobfinder.session import get_working_df
from jobfinder.utils import get_now

logger = logging.getLogger(__name__)


def render_header():
    st.title("💼 jobfinder")
    st.markdown("---")

    if not get_working_df().empty:
        _render_stats()
    render_sidebar()


def check_working_df():
    if get_working_df().empty:
        st.warning("No jobs found. Please scrape new jobs for page functionality.")
        st.stop()


def render_footer():
    st.markdown("---")
    _col_left, _col_right = st.columns([1, 2])
    with _col_left:
        st.markdown(f"jobfinder v{__version__}")
    with _col_right:
        st.markdown(f"Loaded:{get_now()}")


def _render_stats():
    logger.info("Rendering display stats")
    st.subheader("Statistics")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Jobs", st.session_state.stats.total_jobs)
    col2.metric("New Jobs", st.session_state.stats.new_jobs)
    col3.metric("Excluded Jobs", st.session_state.stats.excluded_jobs)
    col4.metric("Summarized Jobs", st.session_state.stats.summarized_jobs)
    col5.metric("Scored Jobs", st.session_state.stats.scored_jobs)


def render_sidebar():
    st.sidebar.page_link("main.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/scrape_jobs.py", label="Scrape New Jobs", icon="🔍")
    st.sidebar.page_link("pages/job_details.py", label="Job Details", icon="📋")
    st.sidebar.page_link("pages/scoring_util.py", label="Scoring Utility", icon="🤖")
    st.sidebar.page_link("pages/insert_record.py", label="Insert Record", icon="➕")
    st.sidebar.page_link("pages/data_management.py", label="Data Management", icon="⚙️")


# MAIN_TABS = [
#     "📊 Job Overview",
#     # " Add Record",
#     # "📝 Summarization Util",
#     " Scoring Util",
#     # "⚙️ Data Management",
# ]
