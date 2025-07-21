from jobfinder.domain.models import APPLIED, EXCLUDED, NEW, VIEWED
from jobfinder.session import get_data_service


def render(st):
    st.subheader("Statistics")
    # TODO: Readd statistics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("New Jobs", _get_count_for_status(NEW))
    col2.metric("Viewed Jobs", _get_count_for_status(VIEWED))
    col3.metric("Excluded Jobs", _get_count_for_status(EXCLUDED))
    col4.metric("Applied Jobs", _get_count_for_status(APPLIED))


def _get_count_for_status(status: str) -> int:
    return get_data_service().get_count(status=status)
    # if get_jobs_df().empty:
    #     return 0
    # return len(get_jobs_df()[get_jobs_df()["status"] == status.value])
