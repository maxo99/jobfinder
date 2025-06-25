import pandas as pd

from jobspy import scrape_jobs

from jobfinder.utils import get_now
from jobfinder.utils.persistence import save_data, update_results, validate_defaults
from jobfinder import st 

SITES = ['indeed', 'linkedin']


def render():
    
    # Search parameters
    search_term = st.text_input("Search Term", value="python developer")
    site_name = st.multiselect("Sites", SITES, default=SITES)
    results = st.number_input("Results", min_value=1, max_value=1000, value=2)
    hours_old = st.number_input("Age", min_value=1, max_value=480, value=72)

    # Scrape button
    if st.button("🚀 Scrape Jobs", type="primary"):
        new_jobs = _find_jobs(
            site_name=site_name,
            search_term=search_term,
            results_wanted=results,
            hours_old=hours_old,
        )
        if not new_jobs.empty:
            
            if not st.session_state.jobs_df.empty:
                update_results(new_jobs)
            else:
                st.session_state.jobs_df = new_jobs

            save_data(st.session_state.jobs_df)
            st.rerun()


def _find_jobs(
    site_name: list[str],
    search_term: str,
    results_wanted: int,
    hours_old: int,
):

    try:
        with st.spinner(f"Scraping {results_wanted} jobs from {site_name}..."):

            jobs = scrape_jobs(
                site_name=site_name,
                search_term=search_term,
                results_wanted=results_wanted,
                hours_old=hours_old,
                is_remote=True,
                country_indeed="USA",
                linkedin_fetch_description=True,
            )

            if jobs is not None and not jobs.empty:
                validate_defaults(jobs)
                return jobs
            else:
                st.warning("No jobs found with the specified criteria.")
                return pd.DataFrame()

    except Exception as e:
        st.error(f"Error scraping jobs: {e}")
        return pd.DataFrame()
