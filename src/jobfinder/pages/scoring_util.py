import logging

from jobfinder.domain.constants import DEFAULT_COLS, DISPLAY_COLS
from jobfinder.domain.models import df_to_jobs
from jobfinder.session import (
    chat_enabled,
    get_current_prompt,
    get_data_service,
    get_generative_service,
    get_selected_records,
    get_working_df,
    set_selected_data,
)
from jobfinder.utils.service_helpers import render_jinja

logger = logging.getLogger(__name__)

SCORING_UTIL_DESCRIPTION = """
    Select a listing to use for evaluation.
    Select records to populate as prompt context using Jinja2 templates.
"""


def render(st):
    st.subheader("Scoring Utility")
    st.markdown(SCORING_UTIL_DESCRIPTION)
    st.subheader("Select Listing")

    working_df = get_working_df().copy()

    _keys = working_df["id"].astype(str).tolist()
    _key = st.selectbox(
        "Select a Listing for Scoring",
        options=_keys,
        format_func=lambda x: working_df.loc[working_df["id"] == x]["name"].iloc[0],
        key="select_listing_scoring",
        index=0,
    )
    # if _key:
    #     logger.info(
    #         f"Selected job:{_key}: {working_df.loc[working_df['id'] == _key]['name'].iloc[0]}"
    #     )
    # else:
    #     _key = _keys[0]
    current_selected = working_df.loc[working_df["id"] == _key]

    st.subheader("Select Sample Records")

    selection_df = working_df.copy()[DISPLAY_COLS]

    try:
        selected_rows = st.dataframe(
            selection_df,
            use_container_width=True,
            on_select="rerun",
            column_order=DEFAULT_COLS,
            selection_mode="multi-row",
            key="scoring_selection_dataframe",
        )

        if (
            selected_rows
            and "selection" in selected_rows
            and "rows" in selected_rows["selection"]
        ):
            selected_indices = selected_rows["selection"]["rows"]
            set_selected_data([selection_df.iloc[i]["id"] for i in selected_indices])
    except Exception as e:
        logger.error("Error rendering dataframe: %s", e)
        st.error("Error rendering dataframe. Please check the logs.")

    _current_prompt = get_current_prompt()

    _selected_data = get_selected_records()

    if _selected_data and _current_prompt:
        _scoring_job = df_to_jobs(current_selected)[0]
        rendered_prompt = render_jinja(
            template_str=_current_prompt,
            data={
                "records": _selected_data,
                "listing": _scoring_job.model_dump(),
            },
        )

        # Show preview
        st.code(rendered_prompt, language="markdown")

        if st.button("Generate Score", use_container_width=True, key="gen_score"):
            if not chat_enabled():
                st.error("Chat not enabled, see README for configuration")
            try:
                _scoring_job = get_generative_service().generate_score(
                    st, _scoring_job, rendered_prompt=rendered_prompt
                )
            except Exception as e:
                logger.error("Error generating score: %s", e)
                st.error("Error generating score. Please check the logs.")
                return
            if not _scoring_job:
                st.error("Failed to generate score. Please check the logs.")
                return
            get_data_service().store_jobs([_scoring_job])
            st.success("Score generated and updated successfully!")
            st.rerun()

    else:
        st.subheader("👀 Template Preview")
        st.code(get_current_prompt(), language="markdown")
        st.info("Select sample records from the panel to populate template")
