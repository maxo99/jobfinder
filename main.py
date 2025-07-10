import logging

from jobfinder import __version__, _setup_logging
from jobfinder.bootstrap import load_backend
from jobfinder.session import st, _init_session
from jobfinder.utils import get_now
from jobfinder.views import (
    data_management,
    display_filters,
    find_jobs,
    individual_job_details,
    listings_overview,
    scoring_util,
    add_record,
    summarization_util,
    display_stats,
)


logger = logging.getLogger(__name__)




MAIN_TABS = [
    "📊 Job Overview",
    "📋 Job Details",
    "➕ Add Record",
    "📝 Summarization Util",
    "🤖 Scoring Util",
    "⚙️ Data Management",
]


def main():
    logging.info("Starting up main()")

    st.set_page_config(page_title="jobfinder", page_icon="💼", layout="wide")

    _setup_logging()
    load_backend()
    _init_session()

    # Main app
    st.title("💼 jobfinder")
    st.markdown("---")
    display_stats.render()


    # Sidebar for scraping configuration
    with st.sidebar:
        with st.expander("🔍 Find Jobs", expanded=True):
            find_jobs.render()
        with st.expander("🔧 Display Filters", expanded=False):
            display_filters.render()

    # Main content area
    if not st.session_state.jobs_df.empty:


        jo, jd, ar, summ, sco, dm = st.tabs(MAIN_TABS)

        with jo:
            st.header("Job Listings Overview")
            listings_overview.render()

        with jd:
            st.header("Individual Job Details")
            individual_job_details.render()

        with ar:
            st.header("Add Record")
            add_record.render()

        with summ:
            summarization_util.render()

        with sco:
            st.header("Job Scoring Utility")
            scoring_util.render()

        with dm:
            st.header("Data Management")
            data_management.render()

    else:
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
