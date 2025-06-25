import streamlit as st
import pandas as pd
from jobspy import scrape_jobs
import os
from datetime import datetime
import json

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
    st.session_state.job_data_file = 'jobs_data.csv'

def load_existing_data():
    """Load existing job data if it exists"""
    if os.path.exists(st.session_state.job_data_file):
        try:
            df = pd.read_csv(st.session_state.job_data_file)
            # Ensure required columns exist
            if 'viewed' not in df.columns:
                df['viewed'] = False
            if 'notes' not in df.columns:
                df['notes'] = ''
            if 'date_scraped' not in df.columns:
                df['date_scraped'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return df
        except Exception as e:
            st.error(f"Error loading existing data: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

def save_data(df):
    """Save dataframe to CSV"""
    try:
        df.to_csv(st.session_state.job_data_file, index=False)
        st.success("Data saved successfully!")
    except Exception as e:
        st.error(f"Error saving data: {e}")

def scrape_jobs_wrapper(site_name, search_term, location, results_wanted, hours_old, country_indeed):
    """Wrapper function for job scraping with error handling"""
    try:
        with st.spinner(f"Scraping {results_wanted} jobs from {site_name}..."):
            jobs = scrape_jobs(
                site_name=[site_name] if isinstance(site_name, str) else site_name,
                search_term=search_term,
                location=location,
                results_wanted=results_wanted,
                hours_old=hours_old,
                country_indeed=country_indeed
            )
            
            if jobs is not None and not jobs.empty:
                # Add tracking columns
                jobs['viewed'] = False
                jobs['notes'] = ''
                jobs['date_scraped'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return jobs
            else:
                st.warning("No jobs found with the specified criteria.")
                return pd.DataFrame()
                
    except Exception as e:
        st.error(f"Error scraping jobs: {e}")
        return pd.DataFrame()

def main():
    # Main app
    st.title("💼 Job Scraper & Manager")
    st.markdown("---")

    # Load existing data on startup
    if st.session_state.jobs_df.empty:
        st.session_state.jobs_df = load_existing_data()

    # Sidebar for scraping configuration
    with st.sidebar:
        st.header("🔍 Job Scraping Configuration")
        
        # Site selection
        site_options = ['indeed', 'linkedin', 'zip_recruiter', 'glassdoor']
        site_name = st.selectbox("Select Job Site", site_options)
        
        # Search parameters
        search_term = st.text_input("Search Term", value="python developer")
        location = st.text_input("Location", value="United States")
        results_wanted = st.number_input("Number of Jobs", min_value=1, max_value=1000, value=50)
        hours_old = st.number_input("Max Hours Old", min_value=1, max_value=168, value=72)
        
        # Country for Indeed
        country_indeed = 'USA'
        if site_name == 'indeed':
            country_options = ['USA', 'Canada', 'UK', 'Australia', 'Germany', 'France']
            country_indeed = st.selectbox("Indeed Country", country_options)
        
        # Scrape button
        if st.button("🚀 Scrape Jobs", type="primary"):
            new_jobs = scrape_jobs_wrapper(site_name, search_term, location, results_wanted, hours_old, country_indeed)
            if not new_jobs.empty:
                # Combine with existing data
                if not st.session_state.jobs_df.empty:
                    # Remove duplicates based on job_url or title+company
                    combined_df = pd.concat([st.session_state.jobs_df, new_jobs], ignore_index=True)
                    if 'job_url' in combined_df.columns:
                        combined_df = combined_df.drop_duplicates(subset=['job_url'], keep='last')
                    else:
                        combined_df = combined_df.drop_duplicates(subset=['title', 'company'], keep='last')
                    st.session_state.jobs_df = combined_df
                else:
                    st.session_state.jobs_df = new_jobs
                
                save_data(st.session_state.jobs_df)
                st.rerun()

    # Main content area
    if not st.session_state.jobs_df.empty:
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["📊 Job Overview", "📋 Job Details", "⚙️ Data Management"])
        
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
            viewed_jobs = len(st.session_state.jobs_df[st.session_state.jobs_df['viewed'] == True])
            unviewed_jobs = total_jobs - viewed_jobs
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Jobs", total_jobs)
            col2.metric("Viewed Jobs", viewed_jobs)
            col3.metric("Unviewed Jobs", unviewed_jobs)
            
            # Display dataframe
            if not filtered_df.empty:
                # Select columns to display
                display_columns = ['title', 'company', 'location', 'job_type', 'date_posted', 'viewed', 'notes']
                available_columns = [col for col in display_columns if col in filtered_df.columns]
                
                st.dataframe(
                    filtered_df[available_columns],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No jobs match the current filters.")
        
        with tab2:
            st.header("Individual Job Details")
            
            if not st.session_state.jobs_df.empty:
                # Job selection dropdown
                job_options = []
                for idx, row in st.session_state.jobs_df.iterrows():
                    status = "✅" if row.get('viewed', False) else "⭕"
                    job_options.append(f"{status} {row.get('title', 'No Title')} - {row.get('company', 'No Company')} (Row {idx})")
                
                selected_job = st.selectbox("Select a Job", job_options)
                
                if selected_job:
                    # Extract row index from selection
                    row_idx = int(selected_job.split('(Row ')[-1].split(')')[0])
                    job_row = st.session_state.jobs_df.iloc[row_idx]
                    
                    # Display job details
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader(f"📝 {job_row.get('title', 'No Title')}")
                        st.write(f"**Company:** {job_row.get('company', 'N/A')}")
                        st.write(f"**Location:** {job_row.get('location', 'N/A')}")
                        st.write(f"**Job Type:** {job_row.get('job_type', 'N/A')}")
                        st.write(f"**Date Posted:** {job_row.get('date_posted', 'N/A')}")
                        st.write(f"**Salary:** {job_row.get('min_amount', 'N/A')} - {job_row.get('max_amount', 'N/A')} {job_row.get('currency', '')}")
                        
                        # Job URL
                        if 'job_url' in job_row and pd.notna(job_row['job_url']):
                            st.markdown(f"**Job URL:** [View Job]({job_row['job_url']})")
                        
                        # Job description
                        if 'description' in job_row and pd.notna(job_row['description']):
                            st.subheader("Job Description")
                            st.write(job_row['description'][:1000] + "..." if len(str(job_row['description'])) > 1000 else job_row['description'])
                    
                    with col2:
                        st.subheader("Actions")
                        
                        # Viewed status
                        current_viewed = job_row.get('viewed', False)
                        new_viewed = st.checkbox("Mark as Viewed", value=current_viewed, key=f"viewed_{row_idx}")
                        
                        # Notes
                        current_notes = job_row.get('notes', '')
                        new_notes = st.text_area("Notes", value=current_notes, key=f"notes_{row_idx}")
                        
                        # Update button
                        if st.button("💾 Update Job", key=f"update_{row_idx}"):
                            st.session_state.jobs_df.loc[row_idx, 'viewed'] = new_viewed
                            st.session_state.jobs_df.loc[row_idx, 'notes'] = new_notes
                            save_data(st.session_state.jobs_df)
                            st.success("Job updated successfully!")
                            st.rerun()
                        
                        # Delete button
                        if st.button("🗑️ Delete Job", key=f"delete_{row_idx}", type="secondary"):
                            st.session_state.jobs_df = st.session_state.jobs_df.drop(row_idx).reset_index(drop=True)
                            save_data(st.session_state.jobs_df)
                            st.success("Job deleted successfully!")
                            st.rerun()
        
        with tab3:
            st.header("Data Management")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Export Data")
                if st.button("📥 Download CSV"):
                    csv_data = st.session_state.jobs_df.to_csv(index=False)
                    st.download_button(
                        label="Download jobs data as CSV",
                        data=csv_data,
                        file_name=f"jobs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                st.subheader("Clear Data")
                if st.button("🗑️ Clear All Data", type="secondary"):
                    if st.button("⚠️ Confirm Clear All", key="confirm_clear"):
                        st.session_state.jobs_df = pd.DataFrame()
                        if os.path.exists(st.session_state.job_data_file):
                            os.remove(st.session_state.job_data_file)
                        st.success("All data cleared!")
                        st.rerun()
            
            # Data file management
            st.subheader("Data File")
            st.write(f"Current data file: `{st.session_state.job_data_file}`")
            
            # Bulk actions
            st.subheader("Bulk Actions")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Mark All as Viewed"):
                    st.session_state.jobs_df['viewed'] = True
                    save_data(st.session_state.jobs_df)
                    st.success("All jobs marked as viewed!")
                    st.rerun()
            
            with col2:
                if st.button("Mark All as Unviewed"):
                    st.session_state.jobs_df['viewed'] = False
                    save_data(st.session_state.jobs_df)
                    st.success("All jobs marked as unviewed!")
                    st.rerun()

    else:
        # Welcome screen
        st.info("👋 Welcome! Use the sidebar to configure your job search and start scraping.")
        st.markdown("""
        ### Getting Started:
        1. **Configure your search** in the sidebar
        2. **Select a job site** (Indeed, LinkedIn, ZipRecruiter, Glassdoor)
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



def main():
    print("Hello from jobfinder!")



if __name__ == "__main__":
    main()
