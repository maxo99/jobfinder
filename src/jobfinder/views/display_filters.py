import logging
from jobfinder.session import (
    apply_status_filters,
    apply_title_filters,
    get_filtered_jobs_df,
    get_title_filters,
    set_status_filter,
    set_title_filters,
)
from jobfinder.model import DEFAULT_STATUS_FILTERS, STATUS_OPTIONS


logger = logging.getLogger(__name__)


def render(st):
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
        placeholder="e.g. 'Engineer, Scientist'",
    )
    if new_titles:
        logger.info(f"Adding title filters: {new_titles}")
        new_titles = [t.strip() for t in new_titles.split(",")]
        set_title_filters([*get_title_filters(), *new_titles])
        apply_title_filters(get_filtered_jobs_df())

    st.write(f"Current Title Filters:{', '.join(get_title_filters())}")

    if st.button("Clear Title Filters"):
        logger.info("Clearing title filters.")
        set_title_filters([])
        apply_title_filters(get_filtered_jobs_df())
