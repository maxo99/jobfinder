# import logging

# import pandas as pd

# from jobfinder.domain.models import AI, USER, df_to_jobs
# from jobfinder.session import (
#     chat_enabled,
#     get_data_service,
#     get_generative_service,
#     get_working_df,
# )
# from jobfinder.utils import get_now
# from jobfinder.views.listings_overview import DEFAULT_COLS, DISPLAY_COLS

# logger = logging.getLogger(__name__)


# def render(st):
#     st.subheader("Summarize Jobs")
#     df_display = get_working_df().copy()


#     selected_rows = st.dataframe(
#         df_display[DISPLAY_COLS].copy(),
#         use_container_width=True,
#         on_select="rerun",
#         column_order=DEFAULT_COLS,
#         selection_mode="multi-row",
#         key="summarization_selection_dataframe",
#     )

#     selected_df = _get_selected_df(df_display, selected_rows)

#     if selected_df.empty:
#         st.warning("Please select one or more jobs to summarize.")
#     else:
#         summarization_mode = st.radio(
#             "Summarization Mode",
#             [AI, USER],
#             horizontal=True,
#             key="summarize_jobs_mode",
#         )
#         # _selected_data = selected_df.to_dict("records")

#         if summarization_mode == AI:
#             st.info("AI will generate summaries for the selected jobs.")
#             if st.button("Generate AI Summaries"):
#                 with st.spinner(f"Generating {len(selected_df.index)} summaries...", show_time=True):
#                     result = get_generative_service().summarize_jobs(selected_df)
#                     if isinstance(result, pd.DataFrame):
#                         st.success("Record summarized successfully!")
#                         get_data_service().store_jobs(df_to_jobs(result))
#                         st.rerun()
#                     else:
#                         st.error(
#                             "No content returned from AI completion. "
#                             "Please check the prompt."
#                         )
#         elif summarization_mode == USER:
#             st.info("You will provide a summary for the selected jobs.")

#             with st.form("user summarization form"):
#                 st.write("Set summary for one or many jobs at once.")

#                 new_summary = st.text_area("summary")
#                 submit = st.form_submit_button("Submit")
#                 if submit:
#                     st.text("Submitted")
#                     selected_df["summarizer"] = USER
#                     selected_df["summary"] = new_summary
#                     selected_df["modified"] = get_now()
#                     get_data_service().store_jobs(df_to_jobs(selected_df))
#                     st.success("Record added successfully!")
#                     st.rerun()

# def _get_selected_df(df_display: pd.DataFrame, selected_rows: dict) -> pd.DataFrame:
#     selected_df = pd.DataFrame()
#     if (
#         selected_rows
#         and "selection" in selected_rows
#         and "rows" in selected_rows["selection"]
#     ):
#         selected_indices = selected_rows["selection"]["rows"]
#         _selected_data_records = [df_display.iloc[i]["id"] for i in selected_indices]

#         selected_df = df_display[df_display["id"].isin(_selected_data_records)]
#     return selected_df


# # def _actions(job: FoundJob, idx: int):
# #     st.subheader("Actions")

# #     _current_status = job.status.value
# #     new_status = st.selectbox(
# #         "Update Status",
# #         options=[s.value for s in Status],
# #         index=[s.value for s in Status].index(_current_status),
# #         key=f"status_{idx}",
# #     )
# #     new_pros = st.text_area("Pros", value=job.pros)
# #     new_cons = st.text_area("Cons", value=job.cons)
# #     new_summary = st.text_area("Summary", value=job.summary)

# #     new_score = st.number_input(
# #         "Score (0.0 - 10.0)",
# #         value=job.score,
# #         min_value=float(0),
# #         max_value=float(10),
# #         key=f"score_{idx}",
# #     )

# #     if new_pros != job.pros or new_cons != job.cons or new_score != job.score:
# #         _classifier = UserType.USER.value
# #     else:
# #         _classifier = UserType(job.classifier).value
# #     if new_summary != job.summary:
# #         _summarizer = UserType.USER.value
# #     else:
# #         _summarizer = UserType(job.summarizer).value

# #     if st.button("💾 Update Job"):
# #         # Automatically set to VIEWED if NEW
# #         if new_status == Status.NEW.value:
# #             new_status = Status.VIEWED.value
# #         get_jobs_df().loc[idx, "status"] = new_status
# #         get_jobs_df().loc[idx, "pros"] = new_pros
# #         get_jobs_df().loc[idx, "cons"] = new_cons
# #         get_jobs_df().loc[idx, "score"] = new_score
# #         get_jobs_df().loc[idx, "summary"] = new_summary
# #         get_jobs_df().loc[idx, "classifier"] = _classifier
# #         get_jobs_df().loc[idx, "summarizer"] = _summarizer
# #         get_jobs_df().loc[idx, "modified"] = get_now()
# #         save_data2(get_jobs_df())
# #         st.success("Job updated successfully!")
# #         st.rerun()

# #     # # Delete button
# #     # if st.button("🗑️ Delete Job", key=f"delete_{idx}", type="secondary"):
# #     #     _delete(idx)
# #     #     st.rerun()


# # def get_selected_records() -> list[dict]:
# #     if not st.session_state.selected_records:
# #         return []

# #     selected_df = get_jobs_df()[
# #         get_jobs_df()["id"].isin(st.session_state.selected_records)
# #     ]
# #     return selected_df.to_dict("records")


# # def set_selected_data(record_ids: list[str]):
# #     st.session_state.selected_records = record_ids
