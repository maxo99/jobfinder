import pandas as pd
from jobfinder import DATA_DIR, st
import logging
from jobfinder.views import data_management, find_jobs, individual_job_details, listings_overview
from jobfinder.utils.persistence import load_existing_data, update_results


logger = logging.getLogger(__name__)

def _init_session():
    if 'jobs_df' not in st.session_state:
        st.session_state.jobs_df = pd.DataFrame()
    if 'job_data_file' not in st.session_state:
        st.session_state.job_data_file = str(DATA_DIR.joinpath('jobs_data.csv'))
    if st.session_state.jobs_df.empty:
        st.session_state.jobs_df = load_existing_data()
    if 'filtered_jobs' not in st.session_state:
        st.session_state.filtered_jobs = st.session_state.jobs_df.copy()


def main():
    logging.info("Starting up main()")
    # Configure the page
    st.set_page_config(
        page_title="Job Scraper & Manager",
        page_icon="💼",
        layout="wide"
    )

    # Initialize session state
    _init_session()

    # Main app
    st.title("💼 Job Scraper & Manager")
    st.markdown("---")

    # Sidebar for scraping configuration
    with st.sidebar:
        st.header("🔍 Find Jobs")
        find_jobs.render()

    # Main content area
    if not st.session_state.jobs_df.empty:
        # Create tabs
        tab1, tab2, tab3 = st.tabs(
            [
                "📊 Job Overview",
                "📋 Job Details",
                "⚙️ Data Management"
            ]
        )

        with tab1:
            st.header("Job Listings Overview")
            listings_overview.render()

        with tab2:
            st.header("Individual Job Details")
            individual_job_details.render()

        with tab3:
            st.header("Data Management")
            data_management.render()

    else:
        # Welcome screen
        st.info(
            "👋 Welcome! Use the sidebar to configure your job search and start scraping.")
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
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit and JobSpy")


if __name__ == "__main__":
    main()
