import logging

from jobfinder.domain.models import APPLIED, EXCLUDED, NEW, VIEWED
from jobfinder.session import get_data_service

logger = logging.getLogger(__name__)


def render(st):


    logger.info("Rendering display stats")
    st.subheader("Statistics")
    
    # col1, col2, col3 = st.columns(3)
    # placeholder1 = col1.empty()
    # placeholder2 = col2.empty()
    # placeholder3 = col3.empty()

    # # Update metrics dynamically
    # placeholder1.metric("Temperature", "70 °F", "1.2 °F")
    # placeholder2.metric("Wind", "9 mph", "-8%")
    # placeholder3.metric("Humidity", "86%", "4%")



    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Jobs", get_data_service().get_count())
    col2.metric("New Jobs", _get_count_for_status(NEW))
    col4.metric("Excluded Jobs", _get_count_for_status(EXCLUDED))

    # Summarized jobs 
    # Scored jobs
    # col5.metric("Applied Jobs", _get_count_for_status(APPLIED))


def _get_count_for_status(status: str) -> int:
    return get_data_service().get_count(status=status)
    # if get_jobs_df().empty:
    #     return 0
    # return len(get_jobs_df()[get_jobs_df()["status"] == status.value])
