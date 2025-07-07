import logging
import pandas as pd
from jobfinder.model import Classifier, FoundJob, Status, found_jobs_from_df
from jobfinder.utils import get_now
from jobfinder.utils.persistence import save_data, update_results
from jobfinder import get_jobs_df, set_jobs_df, st

logger = logging.getLogger(__name__)


def render():
    selection_mode = st.radio(
        "Indivudial Record Management",
        ["Update Existing Records", "Add New Record"],
        horizontal=True
    )
    if selection_mode == "Add New Record":
        with st.form("my_form"):
            
            st.write("Manually create records to use for scoring context.")
            title = st.text_area("title")
            pros = st.text_area("pros")
            cons = st.text_area("cons")
            score = st.number_input(
                "Score (0.0 - 10.0)",
                value=5.0,
                min_value=float(0),
                max_value=float(10),
                key="score_new_job"
            )
            submit = st.form_submit_button("Submit")
            if submit:
                st.text("Submitted")
                
                _new_record = pd.DataFrame(
                    {
                        'id': [f"USER_CLASSIFIED_{get_now()}"],
                        'company': ['USER_ADDED'],
                        'title': [title],
                        'pros':[pros],
                        'cons':[cons],
                        'score':[score],
                        'classifier':[Classifier.USER.value],
                        'modified':[get_now()]
                    },

                )
                update_results(_new_record)
                save_data(get_jobs_df())
                st.success("Record added successfully!")
                st.rerun()
    else:
        if not get_jobs_df().empty:
            logger.info(f"Displaying {len(get_jobs_df().index)} Jobs")
            # TODO: IMPROVE ORDERING/FILTERING

            _found_jobs = found_jobs_from_df(get_jobs_df())

            _key = st.selectbox(
                "Select a Job",
                options=list(_found_jobs.keys()),
                format_func=lambda x: _found_jobs[x].name,
                index=0,
            )
            if _key:
                logger.info(f"Selected job:{_key}: {_found_jobs[_key].name}")
            else:
                _key = 0
            _col_details, _col_actions = st.columns([2, 1])
            with _col_details:
                _details(_found_jobs[_key])
            with _col_actions:
                _actions(_found_jobs[_key], _key)


def _details(job: FoundJob):
    st.markdown(job.get_details())


def _actions(job: FoundJob, idx: int):
    st.subheader("Actions")

    _current_status = job.status.value
    new_status = st.selectbox(
        "Update Status",
        options=[s.value for s in Status],
        index=[s.value for s in Status].index(_current_status),
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
        get_jobs_df().loc[idx, "classifier"] = Classifier.USER.value
        get_jobs_df().loc[idx, "modified"] = get_now()
        save_data(get_jobs_df())
        st.success("Job updated successfully!")
        st.rerun()

    # Delete button
    if st.button("🗑️ Delete Job", key=f"delete_{idx}", type="secondary"):
        _delete(idx)
        st.rerun()


def _delete(idx):
    set_jobs_df(get_jobs_df().drop(idx).reset_index(drop=True))
    save_data(get_jobs_df())
    st.success("Job deleted successfully!")
    st.rerun()


def get_user_record_count():
    return 0
