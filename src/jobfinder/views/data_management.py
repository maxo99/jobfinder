import os
import logging
from pandas import DataFrame
from jobfinder import get_jobs_df, get_job_data_file, st
from jobfinder.utils import get_now
from jobfinder.utils.persistence import save_data, validate_defaults

logger = logging.getLogger(__name__)


def render():
    st.subheader("Data File")
    st.write(f"Current data file: `{get_job_data_file()}`")

    _manage_data()
    _bulk_actions()


def _manage_data():
    _col_export_data, _col_clear_data = st.columns(2)

    with _col_export_data:
        st.subheader("Export Data")
        if st.button("📥 Download CSV"):
            csv_data = st.session_state.jobs_df.to_csv(index=False)
            st.download_button(
                label="Download jobs data as CSV",
                data=csv_data,
                file_name=f"jobs_export_{get_now(underscore=True)}.csv",
                mime="text/csv"
            )

    with _col_clear_data:
        st.subheader("Clear Data")
        if st.button("🗑️ Clear All Data"):
            st.session_state.jobs_df = DataFrame()
            st.session_state.filtered_jobs_df = DataFrame()
            if os.path.exists(get_job_data_file()):
                os.remove(get_job_data_file())
                logger.info(f"Cleared : {get_job_data_file()}")
            else:
                logger.warning(f"File not exists:{get_job_data_file()}")
            st.success("All data cleared!")
            st.rerun()


def _bulk_actions():
    st.subheader("Bulk Actions")
    # TODO: Update to mark all as new (just clear status/pros/cons vs new date as well?)

    col1, = st.columns(1)
    with col1:
        if st.button("Mark All as new"):
            validate_defaults(get_jobs_df())
            save_data(get_jobs_df())
            st.success("All jobs marked as new!")
            st.rerun()
