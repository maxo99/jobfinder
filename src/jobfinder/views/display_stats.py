from jobfinder.session import get_jobs_df
from jobfinder.model import Status


def render(st):
    st.subheader("Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("New Jobs", _get_count_for_status(Status.NEW))
    col2.metric("Viewed Jobs", _get_count_for_status(Status.VIEWED))
    col3.metric("Excluded Jobs", _get_count_for_status(Status.EXCLUDED))
    col4.metric("Applied Jobs", _get_count_for_status(Status.APPLIED))


def _get_count_for_status(status: Status) -> int:
    """Get the count of jobs for a specific status."""
    if get_jobs_df().empty:
        return 0
    return len(get_jobs_df()[get_jobs_df()["status"] == status.value])
