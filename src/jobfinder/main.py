import logging

import streamlit as st

from jobfinder import __version__, _setup_logging

# from jobfinder.pages import (
#     display_stats,
#     insert_record,
#     # find_jobs,
#     # individual_job_details,
#     listings_overview,
#     scoring_util,
# )
from jobfinder.session import (
    _init_session,
    _init_working_df,
    # get_working_df,
)
from jobfinder.utils import get_now
from jobfinder.views import display_stats

logger = logging.getLogger(__name__)


MAIN_TABS = [
    "📊 Job Overview",
    # " Add Record",
    # "📝 Summarization Util",
    "🤖 Scoring Util",
    # "⚙️ Data Management",
]


def main():
    logging.info("Starting up main()")

    st.set_page_config(page_title="jobfinder", page_icon="💼", layout="wide")

    if "initialized" not in st.session_state:
        _setup_logging()
        _init_session(st)
    _init_working_df(st)

    # Main app
    st.title("💼 jobfinder")
    st.markdown("---")
    display_stats.render(st)

    # Sidebar for scraping configuration
    # with st.sidebar:
    #     with st.expander("🔍 Find Jobs", expanded=True):
    #         find_jobs.render(st)
    #     # with st.expander("🔧 Display Filters", expanded=False):
    #     #     display_filters.render(st)

    st.sidebar.page_link("pages/find_jobs.py", label="Scrape New Jobs", icon="🔍")
    st.sidebar.page_link("pages/job_details.py", label="Job Details", icon="📋")
    st.sidebar.page_link("pages/insert_record.py", label="Insert Record", icon="➕")
    st.sidebar.page_link("pages/data_management.py", label="Data Management", icon="⚙️")
    st.sidebar.page_link("pages/scoring_util.py", label="Scoring Utility", icon="🤖")

    # # Main content area
    # if not get_working_df().empty:
    #     jo, jd, ar, sco, dm = st.tabs(MAIN_TABS)

    #     with jo:
    #         st.header("Job Listings Overview")
    #         listings_overview.render(st)

    #     # with jd:
    #     #     st.header("Individual Job Details")
    #     #     individual_job_details.render(st)

    #     with ar:
    #         st.header("Add Record")
    #         add_record.render(st)

    #     # with summ:
    #     #     summarization_util.render(st)

    #     with sco:
    #         st.header("Job Scoring Utility")
    #         scoring_util.render(st)

    #     with dm:
    #         st.header("Data Management")
    #         # data_management.render(st)

    # else:
    # Welcome screen
    st.info("Configure your job search and start scraping.")
    st.markdown("""
    ### Getting Started:
    1. **Configure your search** in the sidebar
    2. **Select a job site** (Indeed, LinkedIn)
    3. **Enter search terms** and location
    4. **Click 'Scrape Jobs'** to start collecting job listings
    5. **View and manage** your jobs in the tabs above
    ### Features:
    - 🔍 **Job Scraping**: Collect jobs from multiple sites
    - 📊 **Overview**: View all jobs with filtering options
    - 📋 **Details**: Focus on individual jobs with notes
    - ✅ **Tracking**: Mark jobs as viewed and add personal notes
    - 💾 **Persistence**: Data is automatically saved between sessions
    """)

    # Footer
    _footer()


def _footer():
    st.markdown("---")
    _col_left, _col_right = st.columns([1, 2])
    with _col_left:
        st.markdown(f"jobfinder v{__version__}")
    with _col_right:
        st.markdown(f"Loaded:{get_now()}")


if __name__ == "__main__":
    main()
