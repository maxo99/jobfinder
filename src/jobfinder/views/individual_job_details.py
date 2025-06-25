import pandas as pd
import logging
from jobfinder.model import FoundJob
from jobfinder.utils.persistence import save_data
from jobfinder import st

logger = logging.getLogger(__name__)


def render():

    if not st.session_state.jobs_df.empty:


        # TODO: IMPROVE ORDERING/FILTERING

        job_options = []
        for idx, row in st.session_state.jobs_df.iterrows():
            try:
                _found_job = FoundJob.model_validate(row.to_dict())
                job_options.append(f"{idx}. {_found_job.name}")
            except Exception as e:
                logging.error(f"Failed to convert entry idx:{idx} e:{e}")
                
                
        # Job selection dropdown
        selected_job = st.selectbox("Select a Job", job_options)

        if selected_job:
            # Extract row index from selection

            row_idx = int(selected_job.split(".")[0])
            job_row = st.session_state.jobs_df.iloc[row_idx]

            col1, col2 = st.columns([2, 1])
            with col1:
                _details(job_row)
            with col2:
                _actions(job_row, row_idx)


def _details(job_row):
    st.subheader(f"📝 {job_row.get('title', 'No Title')}")
    st.write(f"**Company:** {job_row.get('company', 'N/A')}")
    st.write(f"**Location:** {job_row.get('location', 'N/A')}")
    st.write(f"**Job Type:** {job_row.get('job_type', 'N/A')}")
    st.write(f"**Date Posted:** {job_row.get('date_posted', 'N/A')}")
    st.write(
        f"**Salary:** {job_row.get('min_amount', 'N/A')} - {job_row.get('max_amount', 'N/A')} {job_row.get('currency', '')}"
    )

    # Job URL

    if "job_url" in job_row and pd.notna(job_row["job_url"]):
        st.markdown(f"**Job URL:** [View Job]({job_row['job_url']})")
    # Job description

    if "description" in job_row and pd.notna(job_row["description"]):
        st.subheader("Job Description")
        st.write(
            job_row["description"][:1000] + "..."
            if len(str(job_row["description"])) > 1000
            else job_row["description"]
        )


def _actions(job_row, idx):
    st.subheader("Actions")

    # Viewed
    current_viewed = job_row.get("viewed", False)
    new_viewed = st.checkbox(
        "Mark as Viewed", value=current_viewed, key=f"viewed_{idx}"
    )

    # Pros
    current_pros = job_row.get("pros", None)
    new_pros = st.text_area("Pros", value=current_pros, key=f"pros_{idx}")

    # Cons
    current_cons = job_row.get("cons", "")
    new_cons = st.text_area("Cons", value=current_cons, key=f"cons_{idx}")

    # Score
    current_score = job_row.get("score", None)
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
