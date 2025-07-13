import logging
from jobfinder.services.scoring_service import generate_score
from jobfinder.session import chat_enabled, get_jobs_df, set_selected_data, get_selected_records

from jobfinder.model import found_jobs_from_df
from jobfinder.utils.service_helpers import render_jinja
from jobfinder.views.listings_overview import DEFAULT_COLS, DISPLAY_COLS

logger = logging.getLogger(__name__)

SCORING_UTIL_DESCRIPTION = """
    Select a listing to use for evaluation.
    Select records to populate as prompt context using Jinja2 templates.
"""


def render(st):
    if not get_jobs_df().empty:
        st.subheader("Scoring Utility")
        st.markdown(SCORING_UTIL_DESCRIPTION)

        st.subheader("Select Listing")
        _found_jobs = found_jobs_from_df(get_jobs_df())

        _keys = list(_found_jobs.keys())
        _key = st.selectbox(
            "Select a Listing for Scoring",
            options=_keys,
            format_func=lambda x: _found_jobs[x].name,
            key="select_listing_scoring",
            index=0,
        )
        if _key:
            logger.info(f"Selected job:{_key}: {_found_jobs[_key].name}")
        else:
            _key = _keys[0]

        st.subheader("Select Sample Records")
        df_display = get_jobs_df().copy()
        selection_df = df_display[DISPLAY_COLS].copy()

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
                set_selected_data(
                    [selection_df.iloc[i]["id"] for i in selected_indices]
                )
        except Exception as e:
            logger.error("Error rendering dataframe: %s", e)
            st.error("Error rendering dataframe. Please check the logs.")

        _current_prompt = st.session_state.get("current_prompt", "")
        _selected_data = get_selected_records()

        if _selected_data and _current_prompt:
            # Render template
            _scoring_job = _found_jobs[_key]
            rendered_prompt = render_jinja(
                template_str=_current_prompt,
                data={
                    "records": _selected_data,
                    "listing": _scoring_job.model_dump(),
                },
            )

            # Show preview
            st.code(rendered_prompt, language="markdown")

            if st.button(
                "Generate Score", use_container_width=True, key="gen_score"
            ):
                if chat_enabled():
                    generate_score(st, _scoring_job, rendered_prompt)
                else:
                    st.error("Chat not enabled, see README for configuration")

        else:
            st.subheader("👀 Template Preview")
            st.code(st.session_state.current_prompt, language="markdown")
            st.info("Select sample records from the panel to populate template")

