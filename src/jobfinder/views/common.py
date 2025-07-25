import logging

import streamlit as st

from jobfinder import __version__
from jobfinder.domain.constants import EXCLUDED, NA, NEW
from jobfinder.session import get_data_service, get_working_df
from jobfinder.utils import get_now

logger = logging.getLogger(__name__)


def render_header():
    st.title("💼 jobfinder")
    st.markdown("---")

    if not get_working_df().empty:
        _render_stats()
    render_sidebar()


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
    col1.metric("Total Jobs", get_data_service().get_count())
    col2.metric("New Jobs", get_data_service().get_count(status=NEW))
    col3.metric("Excluded Jobs", get_data_service().get_count(status=EXCLUDED))
    col4.metric("Summarized Jobs", get_data_service().get_count(not_summarizer=NA))
    col5.metric("Scored Jobs", get_data_service().get_count(not_classifier=NA))


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
