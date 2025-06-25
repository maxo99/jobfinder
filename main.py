import pandas as pd
from jobfinder import st
from jobfinder.utils import get_data_dir
from jobfinder.views import data_management, find_jobs, individual_job_details
from jobfinder.utils.persistence import load_existing_data, update_results


def main():
    # Configure the page
    st.set_page_config(
        page_title="Job Scraper & Manager",
        page_icon="💼",
        layout="wide"
    )

    # Initialize session state
    if 'jobs_df' not in st.session_state:
        st.session_state.jobs_df = pd.DataFrame()
    if 'job_data_file' not in st.session_state:
        st.session_state.job_data_file = f'{get_data_dir()}\jobs_data.csv'

    # Main app
    st.title("💼 Job Scraper & Manager")
    st.markdown("---")

    # Startup Load existing data on startup
    if st.session_state.jobs_df.empty:
        st.session_state.jobs_df = load_existing_data()

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

            # Filter controls
            col1, col2, col3 = st.columns(3)
            with col1:
                show_viewed = st.checkbox("Show Viewed Jobs", value=True)
            with col2:
                show_unviewed = st.checkbox("Show Unviewed Jobs", value=True)
            with col3:
                if st.button("🔄 Refresh Data"):
                    st.rerun()

            # Apply filters
            filtered_df = st.session_state.jobs_df.copy()
            if not show_viewed:
                filtered_df = filtered_df[filtered_df['viewed'] == False]
            if not show_unviewed:
                filtered_df = filtered_df[filtered_df['viewed'] == True]

            # Display stats
            total_jobs = len(st.session_state.jobs_df)
            viewed_jobs = len(
                st.session_state.jobs_df[st.session_state.jobs_df['viewed'] == True])
            unviewed_jobs = total_jobs - viewed_jobs

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Jobs", total_jobs)
            col2.metric("Viewed Jobs", viewed_jobs)
            col3.metric("Unviewed Jobs", unviewed_jobs)

            # Display dataframe
            if not filtered_df.empty:
                # Select columns to display
                display_columns = ['title', 'company', 'location',
                                   'job_type', 'date_posted', 'viewed', 'notes']
                available_columns = [
                    col for col in display_columns if col in filtered_df.columns]

                st.dataframe(
                    filtered_df[available_columns],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No jobs match the current filters.")

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
