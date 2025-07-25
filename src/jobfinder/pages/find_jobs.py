import pandas as pd
import streamlit as st
from jobspy import scrape_jobs

from jobfinder.domain.models import EXCLUDED, df_to_jobs, validate_df_defaults
from jobfinder.session import get_data_service
from jobfinder.utils.persistence import save_data2

SITES = ["indeed", "linkedin"]


# def find_jobs():
# Search parameters
search_term = st.text_input("Search Term", value="python developer")
site_name = st.multiselect("Sites", SITES, default=SITES)
results = st.number_input("Results", min_value=1, max_value=1000, value=2)
hours_old = st.number_input("Age", min_value=1, max_value=480, value=72)

exclude_remote = st.checkbox("Exclude Remote", value=True)
fulltime_only = st.checkbox("Fulltime Only", value=True)


def _find_jobs(
    st,
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
                validate_df_defaults(jobs)
                return jobs
            else:
                st.warning("No jobs found with the specified criteria.")
                return pd.DataFrame()

    except Exception as e:
        st.error(f"Error scraping jobs: {e}")
        return pd.DataFrame()


# Scrape button
if st.button("🚀 Scrape Jobs", type="primary", key="scrape_job"):
    new_jobs = _find_jobs(
        st,
        site_name=site_name,
        search_term=search_term,
        results_wanted=results,
        hours_old=hours_old,
    )
    if new_jobs.empty:
        st.warning("No jobs found with the specified criteria.")
    else:
        if exclude_remote:
            new_jobs.loc[~new_jobs.is_remote, "status"] = EXCLUDED

        if fulltime_only:
            new_jobs.loc[
                ~new_jobs["job_type"].str.contains(
                    "|".join(["fulltime", "full-time"]), case=False, na=False
                ),
                "status",
            ] = EXCLUDED
        st.metric("Pulled Jobs", len(new_jobs.index))

        st.dataframe(new_jobs, use_container_width=True)
        if st.button("Save Scraped Jobs", type="primary", key="save_scraped_jobs"):
            save_data2(new_jobs, state="raw")

            get_data_service().store_jobs(df_to_jobs(new_jobs))
            st.rerun()
