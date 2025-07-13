import json
import logging
import pandas as pd
from jobfinder.utils.persistence import update_results
from jobfinder.session import get_chat_client

from jobfinder.model import UserType, FoundJob
from jobfinder.utils import get_now

logger = logging.getLogger(__name__)


def generate_score(st, scoring_job: FoundJob, rendered_prompt: str):
    _completion = get_chat_client().completions(rendered_prompt)
    _content = str(_completion.choices[0].message.content)
    if not _content:
        st.error("No content returned from AI completion. Please check the prompt.")
        return
    
    if _completion.usage:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Prompt Tokens", _completion.usage.prompt_tokens)
        with col2:
            st.metric("Total Tokens", _completion.usage.total_tokens)


    _x = json.loads(_content)
    scoring_job.score = _x.get("score", 0.0)
    scoring_job.pros = _x.get("pros", "N/A")
    scoring_job.cons = _x.get("cons", "N/A")
    
    col1, col2, col3 = st.columns([0.2, 0.4, 0.4])
    with col1:
        st.metric("Score", scoring_job.score)
    with col2:
        st.markdown("## Pros:")
        st.markdown(scoring_job.pros)
    with col3:
        st.markdown("## Cons:")
        st.markdown(scoring_job.cons)
        
    scoring_job.modified = get_now()
    scoring_job.classifier = UserType.AI
    _updated_entry = pd.DataFrame([scoring_job.model_dump(mode="json")])
    update_results(_updated_entry)
    st.success("Score generated and updated successfully!")
    st.rerun()


