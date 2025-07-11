import pandas as pd

from jobspy import scrape_jobs

from jobfinder.model import Status, validate_defaults
from jobfinder.utils.persistence import save_data2, update_results
from jobfinder.session import st

SITES = ["indeed", "linkedin"]


def render():
    # Search parameters
    search_term = st.text_input("Search Term", value="python developer")
    site_name = st.multiselect("Sites", SITES, default=SITES)
    results = st.number_input("Results", min_value=1, max_value=1000, value=2)
    hours_old = st.number_input("Age", min_value=1, max_value=480, value=72)

    exclude_remote = st.checkbox("Exclude Remote", value=True)
    fulltime_only = st.checkbox("Fulltime Only", value=True)

    # Scrape button
    if st.button("🚀 Scrape Jobs", type="primary", key="scrape_job"):
        new_jobs = _find_jobs(
            site_name=site_name,
            search_term=search_term,
            results_wanted=results,
            hours_old=hours_old,
        )
        if not new_jobs.empty:
            st.metric("Pulled Jobs", len(new_jobs.index))
            save_data2(new_jobs, state="raw")
            if exclude_remote:
                new_jobs.loc[~new_jobs.is_remote, "status"] = Status.EXCLUDED.value

            if fulltime_only:
                new_jobs.loc[
                    ~new_jobs["job_type"].str.contains(
                        "|".join(["fulltime", "full-time"]), case=False, na=False
                    ),
                    "status",
                ] = Status.EXCLUDED.value

            if not st.session_state.jobs_df.empty:
                update_results(new_jobs)
            else:
                validate_defaults(new_jobs)
                st.session_state.jobs_df = new_jobs

            save_data2(st.session_state.jobs_df)
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
