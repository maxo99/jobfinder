import pandas as pd
import logging
from jobfinder.model import FoundJob, Status
from jobfinder.utils.persistence import save_data
from jobfinder import get_jobs_df, set_jobs_df, st

logger = logging.getLogger(__name__)


def render():

    if not get_jobs_df().empty:

        # TODO: IMPROVE ORDERING/FILTERING

        _found_jobs = {
            i: FoundJob.from_dict(d.to_dict())
            for i, d in get_jobs_df().iterrows()
            if FoundJob.from_dict(d.to_dict())
        }

        # Job selection dropdown
        _key = st.selectbox(
            "Select a Job",
            options=list(_found_jobs.keys()),
            format_func=lambda x: _found_jobs[x].name
        )
        if _key:
            logger.info(f"Selected job:{_key}: {_found_jobs[_key].name}")
            _col_details, _col_actions = st.columns([2, 1])
            with _col_details:
                _details(_found_jobs[_key])
            with _col_actions:
                _actions(_found_jobs[_key], _key)


def _details(job: FoundJob):
    st.markdown(job.get_details())


def _actions(job: FoundJob, idx: int):
    st.subheader("Actions")

    new_status = st.selectbox(
        "Status",
        options=[s.value for s in Status],
        placeholder=job.status.value,
        index=0,
        key=f"status_{idx}"
    )
    new_pros = st.text_area("Pros", value=job.pros)
    new_cons = st.text_area("Cons", value=job.cons)

    new_score = st.number_input(
        "Score (0.0 - 10.0)",
        value=job.score,
        min_value=float(0),
        max_value=float(10),
        key=f"score_{idx}"
    )

    if st.button("💾 Update Job"):
        # Automatically set to VIEWED if NEW
        if new_status == Status.NEW.value:
            new_status = Status.VIEWED.value
        get_jobs_df().loc[idx, "status"] = new_status
        get_jobs_df().loc[idx, "pros"] = new_pros
        get_jobs_df().loc[idx, "cons"] = new_cons
        get_jobs_df().loc[idx, "score"] = new_score
        save_data(get_jobs_df())
        st.success("Job updated successfully!")
        st.rerun()

    # Delete button
    if st.button("🗑️ Delete Job", key=f"delete_{idx}", type="secondary"):
        _delete(idx)


def _delete(idx):
    set_jobs_df(get_jobs_df().drop(idx).reset_index(drop=True))
    save_data(get_jobs_df())
    st.success("Job deleted successfully!")
    st.rerun()
