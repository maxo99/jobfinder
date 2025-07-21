import logging

from jobfinder.session import get_working_df

logger = logging.getLogger(__name__)


DEFAULT_COLS = [
    "modified",
    "date_posted",
    "company",
    "title",
    "site",
    "status",
    "summarizer",
    "classifier",
    "score",
    "is_remote",
    "job_type",
]
EXTRA_COLS = ["id", "pros", "cons", "summary"]

JOBSPY_COLS = [
    "id",
    "job_url",
    "job_url_direct",
    "location",
    "salary_source",
    "interval",
    "min_amount",
    "max_amount",
    "currency",
    "job_level",
    "job_function",
    "description",
    "company_industry",
    "company_url",
    "listing_type",
    "emails",
    "company_logo",
    "company_url_direct",
    "company_addresses",
    "company_num_employees",
    "company_revenue",
    "company_description",
    "skills",
    "experience_range",
    "company_rating",
    "company_reviews_count",
    "vacancy_count",
    "work_from_home_type",
]

DISPLAY_COLS = [
    *DEFAULT_COLS,
    #   *JOBSPY_COLS,
    *EXTRA_COLS,
]


def render(st):
    logger.info("Rendering Listings Overview")

    # with st.expander("Filters"):

    _filtered_df = get_working_df().copy()

    # apply_status_filters(_filtered_df)
    # apply_title_filters(_filtered_df)
    # set_filtered_jobs_df(_filtered_df)

    # _total, _filtered = st.columns(2)
    # with _total:
    #     st.write(f"Total Jobs: {len(get_jobs_df())}")
    # with _filtered:
    #     st.write(f"Unfiltered Jobs: {len(get_filtered_jobs_df())}")

    _display_data(st)

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


def _display_data(st):
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
