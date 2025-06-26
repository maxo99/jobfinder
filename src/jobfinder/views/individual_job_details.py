import pandas as pd
import logging
from jobfinder.model import FoundJob
from jobfinder.utils.persistence import save_data
from jobfinder import st

logger = logging.getLogger(__name__)


def render():

    if not st.session_state.jobs_df.empty:


        # TODO: IMPROVE ORDERING/FILTERING


        _found_jobs = {i: FoundJob.from_dict(d.to_dict()) for i, d in st.session_state.jobs_df.iterrows()}
        
        _key = st.selectbox(
            "Select a Job",
            options=list(_found_jobs.keys()),
            format_func=lambda x: _found_jobs[x].name  # Show display name but return key
        )
        
        # Job selection dropdown
        # selected_job = st.selectbox("Select a Job", job_options)

        if _key:
            # Extract row index from selection

            _selected_job = _found_jobs[_key]
            logger.info(f"Selected job: {_selected_job.name} at index {_key}")
            # try:
            col1, col2 = st.columns([2, 1])
            with col1:
                _details(_selected_job)
            with col2:
                _actions(_selected_job, _key)


def _details(job: FoundJob):
    st.markdown(job.get_details())



def _actions(job: FoundJob, idx: int):
    st.subheader("Actions")

    # Viewed
    current_viewed = job.viewed
    new_viewed = st.checkbox(
        "Mark as Viewed", value=current_viewed, key=f"viewed_{idx}"
    )

    # Pros
    current_pros = job.pros
    new_pros = st.text_area("Pros", value=current_pros, key=f"pros_{idx}")

    # Cons
    current_cons = job.cons
    new_cons = st.text_area("Cons", value=current_cons, key=f"cons_{idx}")

    # Score
    current_score = job.score
    logger.info(f"Current job:{idx} score:{current_score} pros:{current_pros} cons:{current_cons}")
    
    new_score = st.number_input(
        "Score (0.0 - 10.0)",
        value=current_score,
        min_value=float(0),
        max_value=float(10),
        key=f"score_{idx}"
    )

    # Update button
    if st.button("💾 Update Job", key=f"update_{idx}"):
        st.session_state.jobs_df.loc[idx, "viewed"] = new_viewed
        st.session_state.jobs_df.loc[idx, "pros"] = new_pros
        st.session_state.jobs_df.loc[idx, "cons"] = new_cons
        st.session_state.jobs_df.loc[idx, "score"] = new_score
        save_data(st.session_state.jobs_df)
        st.success("Job updated successfully!")
        st.rerun()

    # Delete button
    if st.button("🗑️ Delete Job", key=f"delete_{idx}", type="secondary"):
        _delete(idx)


def _delete(idx):
    st.session_state.jobs_df = st.session_state.jobs_df.drop(
        idx).reset_index(drop=True)
    save_data(st.session_state.jobs_df)
    st.success("Job deleted successfully!")
    st.rerun()
