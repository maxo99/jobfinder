import json
import logging
from jinja2 import Template
import pandas as pd
from jobfinder.utils.persistence import update_results
from jobfinder.session import st, get_jobs_df, set_selected_data, get_selected_records
from jobfinder.adapters import chat
from jobfinder.adapters.chat import completions
from jobfinder.model import UserType, found_jobs_from_df, validate_defaults
from jobfinder.utils import get_now
from jobfinder.views.listings_overview import DEFAULT_COLS, DISPLAY_COLS

logger = logging.getLogger(__name__)

SCORING_UTIL_DESCRIPTION = """
    Select a listing to use for evaluation.
    Select records to populate as prompt context using Jinja2 templates.
"""


def render():
    if not get_jobs_df().empty:
        st.subheader("Scoring Utility")
        st.markdown(SCORING_UTIL_DESCRIPTION)

        st.subheader("Select Listing")
        _found_jobs = found_jobs_from_df(get_jobs_df())

        _key = st.selectbox(
            "Select a Listing for Scoring",
            options=list(_found_jobs.keys()),
            format_func=lambda x: _found_jobs[x].name,
            key="select_listing_scoring",
            index=0,
        )
        if _key:
            logger.info(f"Selected job:{_key}: {_found_jobs[_key].name}")
        else:
            _key = 0

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
            rendered_prompt = _render_jinja(
                template_str=_current_prompt,
                data={
                    "records": _selected_data,
                    "listing": _scoring_job.model_dump(),
                },
            )

            # Show preview
            st.code(rendered_prompt, language="markdown")

            if st.button(
                "Generate Score", use_container_width=True, key="generate_score"
            ):
                if chat.enabled:
                    _completion = completions(rendered_prompt)
                    _content = _completion.choices[0].message.content
                    st.code(_content)
                    _x = json.loads(_content)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Prompt Tokens", _completion.usage.prompt_tokens)
                    with col2:
                        st.metric("Total Tokens", _completion.usage.total_tokens)

                    _scoring_job.score = _x.get("score", 0.0)
                    _scoring_job.summary = _x.get("summary", "")
                    _scoring_job.pros = _x.get("pros", "")
                    _scoring_job.cons = _x.get("cons", "")
                    _scoring_job.modified = get_now()
                    _scoring_job.classifier = UserType.AI
                    _updated_entry = pd.DataFrame(
                        [_scoring_job.model_dump(mode="json")]
                    )
                    validate_defaults(_updated_entry)
                    update_results(_updated_entry)
                    st.success("Score generated and updated successfully!")
                    st.rerun()
                else:
                    st.error("Chat not enabled, see README for configuration")

        else:
            st.subheader("👀 Template Preview")
            st.code(st.session_state.current_prompt, language="markdown")
            st.info("Select sample records from the panel to populate template")


def _render_jinja(template_str: str, data: dict) -> str:
    try:
        template = Template(template_str)
        return template.render(**data)
    except Exception as e:
        return f"Template Error: {str(e)}"
