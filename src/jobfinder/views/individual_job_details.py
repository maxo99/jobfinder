import logging
from jobfinder.model import UserType, FoundJob, Status, found_jobs_from_df
from jobfinder.utils import get_now
from jobfinder.utils.persistence import save_data2
from jobfinder.session import get_jobs_df, set_jobs_df, update_by_id

logger = logging.getLogger(__name__)


def render(st):
    # selection_mode = st.radio(
    #     "Indivudial Record Management",
    #     ["Update Existing Records", "Add New Record"],
    #     horizontal=True
    # )
    # if selection_mode == "Add New Record":

    # else:
    if not get_jobs_df().empty:
        logger.info(f"Displaying {len(get_jobs_df().index)} Jobs")
        #  TODO: IMPROVE ORDERING/FILTERING


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
            _key = list(_found_jobs.keys())[0]

        _col_details, _col_actions = st.columns([2, 1])
        with _col_details:
            _details(st, _found_jobs[_key])
        with _col_actions:
            _actions(st, _found_jobs[_key], _key)


def _details(st, job: FoundJob):
    st.markdown(job.get_details())


def _actions(st, job: FoundJob, job_id: str):
    st.subheader("Actions")

    _current_status = job.status.value
    new_status = st.selectbox(
        "Update Status",
        options=[s.value for s in Status],
        index=[s.value for s in Status].index(_current_status),
        key=f"status_{job_id}",
    )
    new_pros = st.text_area("Pros", value=job.pros)
    new_cons = st.text_area("Cons", value=job.cons)
    new_summary = st.text_area("Summary", value=job.summary)

    new_score = st.number_input(
        "Score (0.0 - 10.0)",
        value=job.score,
        min_value=float(0),
        max_value=float(10),
        key=f"score_{job_id}",
    )

    if new_pros != job.pros or new_cons != job.cons or new_score != job.score:
        _classifier = UserType.USER.value
    else:
        _classifier = UserType(job.classifier).value
    if new_summary != job.summary:
        _summarizer = UserType.USER.value
    else:
        _summarizer = UserType(job.summarizer).value

    if st.button("💾 Update Job"):
        # Automatically set to VIEWED if NEW
        if new_status == Status.NEW.value:
            new_status = Status.VIEWED.value
        df = update_by_id(get_jobs_df(), job.id, {
            "status": new_status,
            "pros": new_pros,
            "cons": new_cons,
            "score": new_score,
            "summary": new_summary,
            "classifier": _classifier,
            "summarizer": _summarizer,
            "modified": get_now(),
        })
        set_jobs_df(df)
        save_data2(get_jobs_df())
        st.success("Job updated successfully!")
        st.rerun()

    # Delete button
    if st.button("🗑️ Delete Job", key=f"delete_{job_id}", type="secondary"):
        _delete(st, job_id)
        st.rerun()


def _delete(st, job_id: str):
    set_jobs_df(get_jobs_df().drop(get_jobs_df().index[get_jobs_df()['id'] == job_id]).reset_index(drop=True))
    save_data2(get_jobs_df())
    st.success("Job deleted successfully!")
    st.rerun()


def get_user_record_count():
    return 0
