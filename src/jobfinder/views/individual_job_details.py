import pandas as pd

from jobfinder.model import FoundJob
from jobfinder.utils.persistence import save_data
from jobfinder import st


def render():

    if not st.session_state.jobs_df.empty:
        # Job selection dropdown

        job_options = []

        # TODO: ADD ORDERING/FILTERING

        for idx, row in st.session_state.jobs_df.iterrows():
            try:
                _found_job = FoundJob.model_validate(row.to_dict())
            except Exception as e:
                print(f"Failed to convert entry idx:{idx} e:{e}")
            # status = "✅" if row.get('viewed', False) else "⭕"
            # title = row.get('title', 'No Title')
            # company = row.get('company', 'No Company')

            job_options.append(f"{idx}. {_found_job.name}")
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

    # Viewed status

    current_viewed = job_row.get("viewed", False)
    new_viewed = st.checkbox(
        "Mark as Viewed", value=current_viewed, key=f"viewed_{idx}"
    )

    # Notes
    current_notes = job_row.get("notes", "")
    new_notes = st.text_area("Notes", value=current_notes, key=f"notes_{idx}")

    # Update button
    if st.button("💾 Update Job", key=f"update_{idx}"):
        st.session_state.jobs_df.loc[idx, "viewed"] = new_viewed
        st.session_state.jobs_df.loc[idx, "notes"] = new_notes
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
