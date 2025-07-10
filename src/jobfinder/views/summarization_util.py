import json
import logging
from jobfinder.bootstrap import backend
import pandas as pd
from jinja2 import Template

from jobfinder.constants import SUMMARIZATION_TEMPLATE
from jobfinder.session import get_jobs_df, st

from jobfinder.model import UserType
from jobfinder.utils import get_now
from jobfinder.utils.persistence import update_results
from jobfinder.views.listings_overview import DEFAULT_COLS, DISPLAY_COLS

logger = logging.getLogger(__name__)


def render():
    st.subheader("Summarize Jobs")
    df_display = get_jobs_df().copy()
    selection_df = df_display[DISPLAY_COLS].copy()

    selected_rows = st.dataframe(
        selection_df,
        use_container_width=True,
        on_select="rerun",
        column_order=DEFAULT_COLS,
        selection_mode="multi-row",
        key="summarization_selection_dataframe",
    )

    _selected_data = None
    if (
        selected_rows
        and "selection" in selected_rows
        and "rows" in selected_rows["selection"]
    ):
        selected_indices = selected_rows["selection"]["rows"]
        _selected_data_records = [selection_df.iloc[i]["id"] for i in selected_indices]

        selected_df = df_display[df_display["id"].isin(_selected_data_records)]
        _selected_data = selected_df.to_dict("records")

    if not _selected_data:
        st.warning("Please select one or more jobs to summarize.")
    else:
        summarization_mode = st.radio(
            "Summarization Mode",
            [UserType.AI.value, UserType.USER.value],
            horizontal=True,
            key="summarize_jobs_mode",
        )

        if summarization_mode == UserType.AI.value:
            st.info("AI will generate summaries for the selected jobs.")
            if backend.chat_enabled:
                if st.button("Generate AI Summaries"):
                    st.text("Generating summaries...")
                    summarize_jobs(selection_df)
                    update_results(selection_df)
                    st.success("Record added successfully!")
                    st.rerun()
                else:
                    st.error("Chat not enabled, see README for configuration")
        elif summarization_mode == UserType.USER.value:
            st.info("You will provide a summary for the selected jobs.")

            with st.form("user summarization form"):
                st.write("Set summary for one or many jobs at once.")

                new_summary = st.text_area("summary")
                submit = st.form_submit_button("Submit")
                if submit:
                    st.text("Submitted")
                    selection_df["summarizer"] = UserType.USER.value
                    selection_df["summary"] = new_summary
                    selection_df["modified"] = get_now()
                    update_results(selection_df)
                    st.success("Record added successfully!")
                    st.rerun()


def summarize_jobs(selection_df: pd.DataFrame):
    rendered_prompt = Template(SUMMARIZATION_TEMPLATE).render(
        data={
            "records": selection_df.to_dict("records"),
        }
    )
    _completion = backend.chat_client.completions(rendered_prompt)
    _content = str(_completion.choices[0].message.content)
    if not _content:
        st.error("No content returned from AI completion. Please check the prompt.")
        return
    _x = json.loads(_content)
    for x in _x['summaries']:
        logger.info(f"ID:{x['id']} summary:{x['summary']}")
        mask = selection_df['id'] == x['id']
        if mask.any():
            selection_df.loc[mask, 'summary'] = x['summary']
            selection_df.loc[mask, "summarizer"] = UserType.AI.value
            selection_df.loc[mask, "modified"] = get_now()



# def _actions(job: FoundJob, idx: int):
#     st.subheader("Actions")

#     _current_status = job.status.value
#     new_status = st.selectbox(
#         "Update Status",
#         options=[s.value for s in Status],
#         index=[s.value for s in Status].index(_current_status),
#         key=f"status_{idx}",
#     )
#     new_pros = st.text_area("Pros", value=job.pros)
#     new_cons = st.text_area("Cons", value=job.cons)
#     new_summary = st.text_area("Summary", value=job.summary)

#     new_score = st.number_input(
#         "Score (0.0 - 10.0)",
#         value=job.score,
#         min_value=float(0),
#         max_value=float(10),
#         key=f"score_{idx}",
#     )

#     if new_pros != job.pros or new_cons != job.cons or new_score != job.score:
#         _classifier = UserType.USER.value
#     else:
#         _classifier = UserType(job.classifier).value
#     if new_summary != job.summary:
#         _summarizer = UserType.USER.value
#     else:
#         _summarizer = UserType(job.summarizer).value

#     if st.button("💾 Update Job"):
#         # Automatically set to VIEWED if NEW
#         if new_status == Status.NEW.value:
#             new_status = Status.VIEWED.value
#         get_jobs_df().loc[idx, "status"] = new_status
#         get_jobs_df().loc[idx, "pros"] = new_pros
#         get_jobs_df().loc[idx, "cons"] = new_cons
#         get_jobs_df().loc[idx, "score"] = new_score
#         get_jobs_df().loc[idx, "summary"] = new_summary
#         get_jobs_df().loc[idx, "classifier"] = _classifier
#         get_jobs_df().loc[idx, "summarizer"] = _summarizer
#         get_jobs_df().loc[idx, "modified"] = get_now()
#         save_data2(get_jobs_df())
#         st.success("Job updated successfully!")
#         st.rerun()

#     # # Delete button
#     # if st.button("🗑️ Delete Job", key=f"delete_{idx}", type="secondary"):
#     #     _delete(idx)
#     #     st.rerun()


# def get_selected_records() -> list[dict]:
#     if not st.session_state.selected_records:
#         return []

#     selected_df = get_jobs_df()[
#         get_jobs_df()["id"].isin(st.session_state.selected_records)
#     ]
#     return selected_df.to_dict("records")


# def set_selected_data(record_ids: list[str]):
#     st.session_state.selected_records = record_ids
