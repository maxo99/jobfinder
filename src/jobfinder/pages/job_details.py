import logging

import pandas as pd
import streamlit as st
from streamlit import session_state as ss

from jobfinder.domain.constants import AI, NEW, STATUS_TYPES, USER, VIEWED
from jobfinder.domain.models import Job, df_to_jobs
from jobfinder.session import (
    get_data_service,
    get_generative_service,
    get_working_count,
    get_working_df,
    update_by_id,
)
from jobfinder.utils import get_now
from jobfinder.utils.persistence import save_data2
from jobfinder.views import common

logger = logging.getLogger(__name__)


def _details(job: Job):
    st.markdown(job.get_details())
    expand_details = False
    if job.qualifications:
        st.markdown("## **Qualifications:**")
        st.dataframe(
            data=pd.DataFrame(job.qualifications)[
                ["skill", "experience", "requirement"]
            ],
            use_container_width=True,
            hide_index=True,
        )
        # TODO: IF HAS SCORE
        # if job.score:
        #     st.markdown("## **AI Score:**")
        #     st.write(job.score)

        if st.button("🤖 AI Score Job", key="score_job"):
            ss.scoring_selection = job.id
            st.switch_page("pages/scoring_util.py")

    else:
        expand_details = True

        if st.button("🤖 AI Extract Summarization", key="add_qualifications"):
            with st.spinner("Extracting Qualifications...", show_time=True):
                job.summarizer = AI
                _jobs = [job]
                get_generative_service().extract_qualifications(_jobs)
                get_data_service().embed_populated_jobs(_jobs)
                st.success("Record summarized successfully!")
                st.rerun()

    with st.expander("📖 Job Details", expanded=expand_details):
        if job.description:
            st.markdown("## **Description:**")
            st.markdown(job.description)


def _actions(job: Job, job_id: str):
    st.subheader("Actions")

    _current_status = job.status
    new_status = st.selectbox(
        "Update Status",
        options=STATUS_TYPES,
        index=list(STATUS_TYPES).index(_current_status),
        key=f"status_{job_id}",
    )
    new_pros = st.text_area("Pros", value=job.pros)
    new_cons = st.text_area("Cons", value=job.cons)
    new_summary = st.text_area("Summary", value=job.summary)

    new_score = st.number_input(
        "Score (-1.0 - 1.0)",
        value=job.score,
        min_value=float(-1),
        max_value=float(1),
        key=f"score_{job_id}",
    )

    if new_pros != job.pros or new_cons != job.cons or new_score != job.score:
        _classifier = USER
    else:
        _classifier = job.classifier
    if new_summary != job.summary:
        _summarizer = USER
    else:
        _summarizer = job.summarizer

    if st.button("💾 Update Job", key="update_individual_job"):
        # Automatically set to VIEWED if NEW
        if new_status == NEW:
            new_status = VIEWED
        df = update_by_id(
            get_working_df(),
            job.id,
            {
                "status": new_status,
                "pros": new_pros,
                "cons": new_cons,
                "score": new_score,
                "summary": new_summary,
                "classifier": _classifier,
                "summarizer": _summarizer,
                "modified": get_now(),
            },
        )
        get_data_service().store_jobs(df_to_jobs(df))
        save_data2(get_working_df())
        st.success("Job updated successfully!")
        st.rerun()

    # Delete button
    if st.button("🗑️ Delete Job", key=f"delete_{job_id}", type="secondary"):
        _delete(job_id)
        st.rerun()


def _delete(job_id: str):
    get_data_service().delete_job(job_id)
    st.success("Job deleted successfully!")
    st.rerun()


# selection_mode = st.radio(
#     "Indivudial Record Management",
#     ["Update Existing Records", "Add New Record"],
#     horizontal=True
# )
# if selection_mode == "Add New Record":

# else:
# if not get_jobs_df().empty:

common.render_header()
common.check_working_df()


logger.info(f"Displaying {get_working_count()} Jobs")
#  TODO: IMPROVE ORDERING/FILTERING

working_df = get_working_df()
_keys = working_df["id"].astype(str).tolist()

_key = st.selectbox(
    "Select a Job",
    options=_keys,
    format_func=lambda x: working_df.loc[working_df["id"] == x]["name"].iloc[0],
    index=0,
)
if _key:
    logger.info(
        f"Selected job:{_key}: {working_df.loc[working_df['id'] == _key]['name'].iloc[0]}"
    )
else:
    _key = _keys[0]

_col_details, _col_actions = st.columns([2, 1])
selection = df_to_jobs(working_df.loc[working_df["id"] == _key])[0]
with _col_details:
    _details(selection)
with _col_actions:
    _actions(selection, _key)

common.render_footer()
