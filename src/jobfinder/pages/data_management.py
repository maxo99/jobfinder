import logging
import os

import streamlit as st

from jobfinder import JOBS_DATA_FILE
from jobfinder.domain.constants import DEFAULT_COLS
from jobfinder.domain.models import Job, df_to_jobs
from jobfinder.session import get_data_service, get_generative_service, get_working_df
from jobfinder.utils import get_now
from jobfinder.views import common

logger = logging.getLogger(__name__)


def _manage_data():
    _col_export_data, _col_clear_data = st.columns(2)

    with _col_export_data:
        st.subheader("Export Data")
        if st.button("📥 Download CSV"):
            csv_data = get_working_df().to_csv(index=False)
            st.download_button(
                label="Download jobs data as CSV",
                data=csv_data,
                file_name=f"jobs_export_{get_now(underscore=True)}.csv",
                mime="text/csv",
            )

    with _col_clear_data:
        st.subheader("Clear Data")
        if st.button("🗑️ Clear All Data"):
            # set_jobs_df(validate_defaults(DataFrame()))
            # reset_filtered_jobs_df()
            if os.path.exists(JOBS_DATA_FILE):
                os.remove(JOBS_DATA_FILE)
                logger.info(f"Cleared : {JOBS_DATA_FILE}")
            else:
                logger.warning(f"File not exists:{JOBS_DATA_FILE}")
            st.success("All data cleared!")
            st.rerun()


def _bulk_actions(jobs: list[Job]):
    st.subheader("Bulk Actions")
    # TODO: Update to mark all as new (just clear status/pros/cons vs new date as well?)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Summarize Jobs"):
            for job in jobs:
                if not job.description:
                    st.warning(f"Job {job.id} has no description to summarize.")
                    continue
                with st.spinner(f"Summarizing {job.name}..."):
                    jobs = [job]
                    get_generative_service().extract_qualifications(jobs)
                    get_data_service().embed_populated_jobs(jobs)
                    st.success("Record summarized successfully!")

            st.success("Jobs summarized successfully!")
            st.rerun()
    with col2:
        if st.button("Reset Jobs"):
            for job in jobs:
                job.reset_job()
            get_data_service().store_jobs(jobs)
            st.success("Jobs have been reset")
            st.rerun()


common.render_header()
st.subheader("Data File")
st.write(f"Current data file: `{JOBS_DATA_FILE}`")
_manage_data()

_working = get_working_df()
if _working.empty:
    st.warning("No jobs found. Please scrape new jobs for page functionality.")
    st.stop()
_s_rows = st.dataframe(
    _working,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="multi-row",
    column_order=DEFAULT_COLS,
    key="data_management_dataframe",
)
_selected_jobs = []
if _s_rows and "selection" in _s_rows and "rows" in _s_rows["selection"]:
    _s_ids = _s_rows["selection"]["rows"]
    _selected_jobs = df_to_jobs(_working.loc[_working["id"].isin(_s_ids)])


st.markdown("---")
if _selected_jobs:
    st.subheader("Selected Records")
    st.write(f"Selected {[job.id for job in _selected_jobs]}")
    st.write(f"Total Selected: {len(_selected_jobs)}")
_bulk_actions(_selected_jobs)
common.render_footer()
