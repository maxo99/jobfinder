import os
import logging
from pandas import DataFrame
from jobfinder import JOBS_DATA_FILE
from jobfinder.session import get_jobs_df, st, reset_filtered_jobs_df, set_jobs_df
from jobfinder.utils import get_now
from jobfinder.model import validate_defaults
from jobfinder.utils.persistence import (
    save_data2,
    update_results,
)

logger = logging.getLogger(__name__)


def render():
    st.subheader("Data File")
    st.write(f"Current data file: `{JOBS_DATA_FILE.name}`")

    _manage_data()
    _bulk_actions()


def _manage_data():
    _col_export_data, _col_clear_data = st.columns(2)

    with _col_export_data:
        st.subheader("Export Data")
        if st.button("📥 Download CSV"):
            csv_data = get_jobs_df().to_csv(index=False)
            st.download_button(
                label="Download jobs data as CSV",
                data=csv_data,
                file_name=f"jobs_export_{get_now(underscore=True)}.csv",
                mime="text/csv",
            )

    with _col_clear_data:
        st.subheader("Clear Data")
        if st.button("🗑️ Clear All Data"):
            set_jobs_df(validate_defaults(DataFrame()))
            reset_filtered_jobs_df()
            if os.path.exists(JOBS_DATA_FILE):
                os.remove(JOBS_DATA_FILE)
                logger.info(f"Cleared : {JOBS_DATA_FILE}")
            else:
                logger.warning(f"File not exists:{JOBS_DATA_FILE}")
            st.success("All data cleared!")
            st.rerun()


def _bulk_actions():
    st.subheader("Bulk Actions")
    # TODO: Update to mark all as new (just clear status/pros/cons vs new date as well?)

    (col1,) = st.columns(1)
    with col1:
        if st.button("Mark All as new"):
            update_results(get_jobs_df())
            save_data2(get_jobs_df())
            st.success("All jobs marked as new!")
            st.rerun()
