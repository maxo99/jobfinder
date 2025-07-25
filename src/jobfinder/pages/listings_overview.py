import logging

# import streamlit as st
from jobfinder.domain.constants import DEFAULT_COLS, DISPLAY_COLS
from jobfinder.session import get_working_df

logger = logging.getLogger(__name__)


# def render(st):

# # with st.expander("Filters"):

# _filtered_df = get_working_df().copy()


def render(st):
    logger.info("Rendering Listings Overview")

    if not get_working_df().empty:
        logger.info("Displaying Filtered Jobs DataFrame")
        st.dataframe(
            data=get_working_df()[DISPLAY_COLS],
            column_order=DEFAULT_COLS,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No jobs match the current filters.")


# _display_data()

# apply_status_filters(_filtered_df)
# apply_title_filters(_filtered_df)
# set_filtered_jobs_df(_filtered_df)

# _total, _filtered = st.columns(2)
# with _total:
#     st.write(f"Total Jobs: {len(get_jobs_df())}")
# with _filtered:
#     st.write(f"Unfiltered Jobs: {len(get_filtered_jobs_df())}")


# _save_changes, _col_refresh = st.columns(2)
# with _save_changes:
#     if st.button("💾 Save Changes"):
#         # Update the original dataframe with the changes
#         _df = get_filtered_jobs_df()
#         _df["classifier"] = UserType.USER.value
#         _df["summarizer"] = UserType.USER.value
#         _df["modified"] = get_now()
#         save_data2(get_jobs_df())
#         st.success("Changes saved successfully!")
#         logger.info("Changes saved successfully!")
#         st.rerun()
# with _col_refresh:
#     if st.button("🔄 Refresh Data"):
#         set_status_filter(DEFAULT_STATUS_FILTERS)
#         set_title_filters([])
#         set_filtered_jobs_df(get_jobs_df().copy())
#         st.rerun()
