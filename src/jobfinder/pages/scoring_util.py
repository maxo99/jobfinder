import logging
import time

import streamlit as st

from jobfinder.domain.constants import (
    DEFAULT_COLS,
    DISPLAY_COLS,
    SCORING_UTIL_DESCRIPTION,
)
from jobfinder.domain.models import df_to_jobs, jobs_to_df
from jobfinder.session import (
    get_current_prompt,
    get_data_service,
    get_generative_service,
    get_working_df,
    # set_selected_data,
    # get_selected_records,
)
from jobfinder.utils.service_helpers import render_jinja
from jobfinder.views import common

logger = logging.getLogger(__name__)

common.render_header()

st.subheader("Scoring Utility 🤖")
st.markdown(SCORING_UTIL_DESCRIPTION)


working_df = get_working_df().copy()
_keys = working_df["id"].astype(str).tolist()


if "scoring_selection" in st.session_state:
    st.markdown("### **Current Selection:**")
    _key = st.session_state.scoring_selection
    st.markdown(working_df.loc[working_df["id"] == _key]["name"].iloc[0])
else:
    st.subheader("Select Listing")
    _key = st.selectbox(
        "Select a Listing for Scoring",
        options=_keys,
        format_func=lambda x: working_df.loc[working_df["id"] == x]["name"].iloc[0],
        key="select_listing_scoring",
        index=0,
    )
current_selected = working_df.loc[working_df["id"] == _key]

# IF NUMBER OF QUALIFIED ....
# SEARCH BY TITLE?

st.subheader("Select Sample Records")
_selected_data = []
similars = get_data_service().search_by_qualifications(
    current_selected["qualifications_vector"].iloc[0]
)
if not similars:
    st.warning("No similar records found. Please select a different listing.")
    st.stop()
logger.info(f"Found {len(similars.jobs)} jobs with scores:{similars.scores}")
selection_df = jobs_to_df(similars.jobs)[DISPLAY_COLS]


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
    _selected_data = [selection_df.iloc[i]["id"] for i in selected_indices]


_current_prompt = get_current_prompt()

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
    st.code(
        rendered_prompt,
        language="markdown",
    )

    if st.button("Generate Score", use_container_width=True, key="gen_score"):
        # if not chat_enabled():

        #     st.error("Chat not enabled, see README for configuration")
        try:
            _scoring_job = get_generative_service().generate_score(
                st, _scoring_job, rendered_prompt=rendered_prompt
            )
            if not _scoring_job:
                raise ValueError("Failed to generate scoring job.")
            get_data_service().store_jobs([_scoring_job])
            st.success("Score generated and updated successfully!")
        except Exception as e:
            logger.error("Error generating score: %s", e)
            st.error("Error generating score. Please check the logs.")
            time.sleep(1)

        st.rerun()

else:
    st.subheader("👀 Template Preview")
    st.code(_current_prompt, language="markdown")
    st.info("Select sample records from the panel to populate template")
common.render_footer()
