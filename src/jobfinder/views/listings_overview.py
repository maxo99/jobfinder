import logging
from jobfinder import (
    apply_status_filters,
    apply_title_filters,
    get_filtered_jobs_df,
    get_jobs_df,
    get_title_filters,
    set_filtered_jobs_df,
    set_status_filter,
    set_title_filters,
    st,
)
from jobfinder.model import DEFAULT_STATUS_FILTERS, STATUS_OPTIONS, Classifier, Status
from jobfinder.utils import get_now
from jobfinder.utils.persistence import save_data2


logger = logging.getLogger(__name__)


DEFAULT_COLS = [
    "modified",
    "date_posted",
    "site",
    "company",
    "title",
    "status",
    "classifier",
    "score",
    "pros",
    "cons",
    "is_remote",
    "job_type",
]

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

DISPLAY_COLS = [*DEFAULT_COLS, *JOBSPY_COLS]


def render():
    logger.info("Rendering Listings Overview")

    with st.expander("Filters"):
        _selected_status = st.multiselect(
            "Status",
            options=STATUS_OPTIONS,
            default=DEFAULT_STATUS_FILTERS,
        )
        if _selected_status:
            # logger.info(f"Applying status filter: {_selected_status}")
            set_status_filter(_selected_status)
            apply_status_filters(get_filtered_jobs_df())

        if st.button("Reset Status Filters"):
            logger.info("Resetting status filters to defaults.")
            set_status_filter(DEFAULT_STATUS_FILTERS)
            apply_status_filters(get_filtered_jobs_df())

        new_titles = st.text_input(
            "Titles Filter (comma-separated)",
            placeholder="Enter titles to filter by, e.g. 'Software Engineer, Data Scientist'",
        )
        if new_titles:
            logger.info(f"Adding title filters: {new_titles}")
            new_titles = [t.strip() for t in new_titles.split(",")]
            set_title_filters([*get_title_filters(), *new_titles])
            apply_title_filters(get_filtered_jobs_df())

        if st.button("Clear Title Filters"):
            logger.info("Clearing title filters.")
            set_title_filters([])
            apply_title_filters(get_filtered_jobs_df())
        st.write(f"Current Title Filters:{','.join(get_title_filters())}")

    _filtered_df = get_filtered_jobs_df()
    apply_status_filters(_filtered_df)
    apply_title_filters(_filtered_df)
    set_filtered_jobs_df(_filtered_df)

    _total, _filtered = st.columns(2)
    with _total:
        st.write(f"Total Jobs: {len(get_jobs_df())}")
    with _filtered:
        st.write(f"Unfiltered Jobs: {len(get_filtered_jobs_df())}")

    _display_data()

    _display_stats()

    _group_operations()



def _display_data():
    if not get_filtered_jobs_df().empty:
        logger.info("Displaying Filtered Jobs DataFrame")
        st.dataframe(
            data=get_filtered_jobs_df()[DISPLAY_COLS],
            column_order=DEFAULT_COLS,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No jobs match the current filters.")


def _group_operations():
    st.subheader("Group Operations")

    _save_changes, _col_refresh = st.columns(2)
    with _save_changes:
        if st.button("💾 Save Changes"):
            # Update the original dataframe with the changes
            _df = get_filtered_jobs_df()
            _df["classifier"] = Classifier.USER.value
            _df["modified"] = get_now()
            save_data2(get_jobs_df())
            st.success("Changes saved successfully!")
            logger.info("Changes saved successfully!")
            st.rerun()
    with _col_refresh:
        if st.button("🔄 Refresh Data"):
            set_status_filter(DEFAULT_STATUS_FILTERS)
            set_title_filters([])
            set_filtered_jobs_df(get_jobs_df().copy())
            st.rerun()

    _set_status, _set_pros = st.columns([0.2, 0.8])
    with _set_status:
        new_status = st.selectbox("Select Status", options=STATUS_OPTIONS)
        if st.button("Set Status"):
            st.success(f"Status updated to {new_status} for selected jobs.")
            filtered_df = get_filtered_jobs_df()
            filtered_df["status"] = new_status
            set_filtered_jobs_df(filtered_df)
            # st.rerun()

    with _set_pros:
        new_pros = st.text_area("Enter Pros")
        if st.button("Set Pros"):
            st.success("Pros updated for selected jobs.")
            filtered_df = get_filtered_jobs_df()
            filtered_df["pros"] = new_pros
            set_filtered_jobs_df(filtered_df)
            # st.rerun()

    _set_score, _set_cons = st.columns([0.2, 0.8])
    with _set_score:
        new_score = st.number_input(
            "Score (0.0 - 10.0)",
            value=float(5.0),
            min_value=float(0),
            max_value=float(10),
            key=f"bulk_set_score",
        )

        if st.button("Set Score"):
            st.success(f"Score updated to {new_score} for selected jobs.")
            filtered_df = get_filtered_jobs_df()
            filtered_df["score"] = new_score
            set_filtered_jobs_df(filtered_df)
            # st.rerun()

    with _set_cons:
        new_cons = st.text_area("Enter Cons")
        if st.button("Set Cons"):
            filtered_df = get_filtered_jobs_df()
            filtered_df["cons"] = new_cons
            st.success(f"Cons updated for selected jobs.")
            set_filtered_jobs_df(filtered_df)
            # st.rerun()


def _display_stats():
    st.subheader("Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("New Jobs", _get_count_for_status(Status.NEW))
    col2.metric("Viewed Jobs", _get_count_for_status(Status.VIEWED))
    col3.metric("Excluded Jobs", _get_count_for_status(Status.EXCLUDED))
    col4.metric("Applied Jobs", _get_count_for_status(Status.APPLIED))


def _get_count_for_status(status: Status) -> int:
    """Get the count of jobs for a specific status."""
    return len(get_jobs_df()[get_jobs_df()["status"] == status.value])
