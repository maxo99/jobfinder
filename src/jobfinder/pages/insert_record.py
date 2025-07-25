import logging

import streamlit as st

from jobfinder.domain.constants import NA, USER
from jobfinder.domain.models import Job
from jobfinder.session import get_data_service
from jobfinder.utils import get_now
from jobfinder.views import common

logger = logging.getLogger(__name__)


common.render_header()
with st.form("my_form"):
    st.write("Manually create records to use for scoring context.")
    title = st.text_area("title")
    summary = st.text_area("summary")
    pros = st.text_area("pros")
    cons = st.text_area("cons")
    score = st.number_input(
        "Score (-1.0 - 1.0)",
        value=0.0,
        min_value=float(-1),
        max_value=float(1),
        key="score_new_job",
    )
    submit = st.form_submit_button("Submit")
    if submit:
        st.text("Submitted")

        if summary:
            _summarizer = USER
        else:
            _summarizer = NA

        if pros or cons or score is not None:
            _classifier = USER
        else:
            _classifier = NA

        _new_record = Job(
            id=f"USER_CREATED_{get_now()}",
            company="USER_ADDED",
            title=title,
            pros=pros,
            summary=summary,
            cons=cons,
            score=score,
            classifier=_classifier,
            summarizer=_summarizer,
            modified=get_now(),
        )
        get_data_service().store_jobs([_new_record])
        st.success("Record added successfully!")
        st.rerun()
common.render_footer()
