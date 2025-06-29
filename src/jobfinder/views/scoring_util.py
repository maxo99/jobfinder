import json

from jobfinder import get_session, st, get_jobs_df
from jobfinder.adapters.chat import completions
from jobfinder.model import FoundJob
from jobfinder.views.listings_overview import DEFAULT_COLS, DISPLAY_COLS
from jinja2 import Template
import logging

logger = logging.getLogger(__name__)


def render():

    if not get_jobs_df().empty:
        st.subheader("Scoring Utility")
        st.markdown(
            """
            This section is intended to provide tools and utilities for scoring and evaluating job listings.
            Select records from the data table and generate system prompts using Jinja2 templates
            """
        )

        st.subheader("Select Listing")
        _found_jobs = {
            i: FoundJob.from_dict(d.to_dict())
            for i, d in get_jobs_df().iterrows()
        }

        _key = st.selectbox(
            "Select a Listing",
            options=list(_found_jobs.keys()),
            format_func=lambda x: _found_jobs[x].name,
            key="select_listing_scoring",
            index=0,
        )
        if _key:
            logger.info(f"Selected job:{_key}: {_found_jobs[_key].name}")
        else:
            _key = 0

        st.subheader("Select Records")
        df_display = get_jobs_df().copy()
        selection_df = df_display[DISPLAY_COLS].copy()

        selected_rows = st.dataframe(
            selection_df,
            use_container_width=True,
            on_select="rerun",
            column_order=DEFAULT_COLS,
            selection_mode="multi-row"
        )

        if selected_rows and 'selection' in selected_rows and 'rows' in selected_rows['selection']:
            selected_indices = selected_rows['selection']['rows']
            set_selected_data(
                [selection_df.iloc[i]['id'] for i in selected_indices]
            )

        st.subheader("👀 Template Preview")

        if get_selected_records():
            # Get selected data
            selected_data = get_selected_records()

            # selection_mode = st.radio(
            #     "Template Preview Mode",
            #     ["Populate All", "Ignore Description"],
            #     horizontal=True
            # )

            # Render template
            rendered_prompt = _render_jinja(
                st.session_state.current_prompt,
                {
                    'records': selected_data,
                    'listing': _found_jobs[_key].model_dump()
                }
            )

            # Show preview
            st.code(rendered_prompt, language="markdown")

            if st.button("Generate Score", use_container_width=True):

                _completion = completions(rendered_prompt)
                _content=_completion.choices[0].message.content
                st.code(_content)
                _x = json.loads(_content)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Prompt Tokens",_completion.usage.prompt_tokens)
                with col2:
                    st.metric("Total Tokens",_completion.usage.total_tokens)

        else:
            st.info("Select records from the left panel to see template preview")


def _render_jinja(template_str: str, data: dict) -> str:
    try:
        template = Template(template_str)
        return template.render(**data)
    except Exception as e:
        return f"Template Error: {str(e)}"


def get_selected_records() -> list[dict]:
    if not st.session_state.selected_records:
        return []

    selected_df = get_jobs_df()[
        get_jobs_df()['id'].isin(st.session_state.selected_records)
    ]
    return selected_df.to_dict('records')


def set_selected_data(record_ids: list[str]):
    st.session_state.selected_records = record_ids
