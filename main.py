import logging
import pandas as pd
from jobfinder import DATA_DIR, reset_filtered_jobs_df, st, __version__
from jobfinder.constants import PRESET_TEMPLATES
from jobfinder.model import DEFAULT_STATUS_FILTERS
from jobfinder.utils import get_now
from jobfinder.views import (
    data_management,
    find_jobs,
    individual_job_details,
    listings_overview,
    scoring_util,
    add_record
)
from jobfinder.utils.persistence import load_existing_data


logger = logging.getLogger(__name__)


def _init_session():
    logger.info("Initializing session")
    if "jobs_df" not in st.session_state:
        st.session_state.jobs_df = pd.DataFrame()
    if "job_data_file" not in st.session_state:
        st.session_state.job_data_file = str(DATA_DIR.joinpath("jobs_data.csv"))
    
    if st.session_state.jobs_df.empty:
        st.session_state.jobs_df = load_existing_data()

    if "saved_prompts" not in st.session_state:
        st.session_state.saved_prompts = PRESET_TEMPLATES

    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = next(
            iter(st.session_state.saved_prompts.values()), ""
        )
    if "selected_records" not in st.session_state:
        st.session_state.selected_records = []

    if "title_filters" not in st.session_state:
        st.session_state.title_filters = []
    if "status_filters" not in st.session_state:
        st.session_state.status_filters = DEFAULT_STATUS_FILTERS

    if "filtered_jobs" not in st.session_state:
        reset_filtered_jobs_df()


def main():
    logging.info("Starting up main()")
    # Configure the page
    st.set_page_config(page_title="jobfinder", page_icon="💼", layout="wide")

    # Initialize session state
    _init_session()

    # Main app
    st.title("💼 jobfinder")
    st.markdown("---")

    # Sidebar for scraping configuration
    with st.sidebar:
        st.header("🔍 Find Jobs")
        find_jobs.render()

    # Main content area
    if not st.session_state.jobs_df.empty:
        # Create tabs
        jo, jd, ar, su, dm = st.tabs(
            [
                "📊 Job Overview",
                "📋 Job Details",
                "➕ Add Record",
                "🤖 Scoring Util",
                "⚙️ Data Management",
            ]
        )

        with jo:
            st.header("Job Listings Overview")
            listings_overview.render()

        with jd:
            st.header("Individual Job Details")
            individual_job_details.render()

        with ar:
            st.header("Add Record")
            add_record.render()

        with su:
            st.header("Job Scoring Utility")
            scoring_util.render()

        with dm:
            st.header("Data Management")
            data_management.render()

    else:
        # Welcome screen
        st.info(
            "👋 Welcome! Use the sidebar to configure your job search and start scraping."
        )
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
