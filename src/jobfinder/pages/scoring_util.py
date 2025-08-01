import logging
import time

import streamlit as st
from streamlit import session_state as ss

from jobfinder.domain.constants import (
    DISPLAY_COLS,
    SCORED_COLS,
    SCORING_UTIL_DESCRIPTION,
)
from jobfinder.domain.models import df_to_jobs, jobs_to_df
from jobfinder.session import (
    get_current_prompt,
    get_data_service,
    get_generative_service,
    get_working_df,
    reload_working_df,
    # set_selected_data,
    # get_selected_records,
)
from jobfinder.utils.service_helpers import render_jinja
from jobfinder.views import common

logger = logging.getLogger(__name__)

common.render_header()
common.check_working_df()

st.subheader("Scoring Utility 🤖")
st.markdown(SCORING_UTIL_DESCRIPTION)


working_df = get_working_df().copy()
_keys = working_df["id"].astype(str).tolist()

st.subheader("Select Listing")
_key = st.selectbox(
    "Select a Listing for Scoring",
    options=_keys,
    format_func=lambda x: working_df.loc[working_df["id"] == x]["name"].iloc[0],
    key="select_listing_scoring",
    index=0,
)


if "scoring_selection" in ss:
    _key = ss.scoring_selection
else:
    _key = _keys[0]

st.markdown("### **Current Selection:**")
st.markdown(working_df.loc[working_df["id"] == _key]["name"].iloc[0])

scoring_job = df_to_jobs(working_df.loc[working_df["id"] == _key])[0]
# IF NUMBER OF QUALIFIED ....
# SEARCH BY TITLE?

st.subheader("Select Sample Records")
if not scoring_job.qualifications:
    st.warning("Please update the listing with qualifications to use this feature.")
    st.stop()
similars = get_data_service().search_by_qualifications(scoring_job)
if not similars:
    st.warning("No similar records found. Please select a different listing.")
    st.stop()
logger.info(f"Found {len(similars.jobs)} jobs with scores:{similars.scores}")
selection_df = jobs_to_df(similars.jobs)[DISPLAY_COLS]

# Adding scores into dataframe for display
selection_df["similarity"] = similars.scores
selection_df = selection_df.sort_values(by="similarity", ascending=False)
selection_df = selection_df.reset_index(drop=True)

_s_rows = st.dataframe(
    selection_df,
    use_container_width=True,
    on_select="rerun",
    column_order=SCORED_COLS,
    selection_mode="multi-row",
    key="scoring_selection_dataframe",
    hide_index=True,
)

_selected_data = []
if _s_rows and "selection" in _s_rows and "rows" in _s_rows["selection"]:
    _s_ids = _s_rows["selection"]["rows"]
    _selected_data = [selection_df.iloc[i]["id"] for i in _s_ids]


_current_prompt = get_current_prompt()

rendered_prompt = render_jinja(
    template_str=_current_prompt,
    data={
        "records": _selected_data,
        "listing": scoring_job.model_dump(),
    },
)


if _selected_data:
    rendered_prompt = render_jinja(
        template_str=_current_prompt,
        data={
            "records": _selected_data,
            "listing": scoring_job.model_dump(),
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
            scoring_job = get_generative_service().generate_score(
                st, scoring_job, rendered_prompt=rendered_prompt
            )
            if not scoring_job:
                raise ValueError("Failed to generate scoring job.")
            get_data_service().store_job(scoring_job)
            st.success("Score generated and updated successfully!")
            reload_working_df()
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
