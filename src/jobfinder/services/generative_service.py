import json
import logging

import pandas as pd
from jinja2 import Template

from jobfinder.adapters.chat.chat_client import ChatClient
from jobfinder.constants import (
    SUMMARIZATION_EXAMPLE_RESPONSE,
    SUMMARIZATION_INSTRUCTIONS,
    SUMMARIZATION_LISTINGS_TEMPLATE,
)
from jobfinder.domain.models import AI, Job, SummarizationResponse
from jobfinder.utils import get_now

logger = logging.getLogger(__name__)


class GenerativeService:
    def __init__(self, chat_client: ChatClient):
        self._chat_client = chat_client

    def generate_score(self, st, scoring_job: Job, rendered_prompt: str) -> Job | None:
        _completion = self._chat_client.completions(rendered_prompt)
        if not _completion.content:
            logger.error("No content returned from AI completion")
            st.error("No content returned. Please check the prompt.")
            return scoring_job

        if _completion.prompt_tokens or _completion.total_tokens:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Prompt Tokens", _completion.prompt_tokens)
            with col2:
                st.metric("Total Tokens", _completion.total_tokens)

        _x = json.loads(_completion.content)
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
        scoring_job.classifier = AI
        return scoring_job

    def summarize_jobs(self, df: pd.DataFrame) -> pd.DataFrame | None:
        try:
            logger.info("Summarizing jobs...")
            rendered_prompt = get_summarization_instruction(df)
            _completion = self._chat_client.completions(rendered_prompt)
            if not _completion.content:
                logger.error("No content returned from AI completion")
                return None

            sr = SummarizationResponse.model_validate_json(_completion.content)
            for id, qualifications in sr.summaries.items():
                logger.info(f"Generated summary for ID:{id}")
                df.loc[df["id"] == id, "summarizer"] = AI
                df.loc[df["id"] == id, "qualifications"] = qualifications
                df.loc[df["id"] == id, "modified"] = get_now()

            return df
        except Exception as e:
            raise e


def get_summarization_instruction(df):
    return (
        SUMMARIZATION_INSTRUCTIONS
        + SUMMARIZATION_EXAMPLE_RESPONSE
        + Template(SUMMARIZATION_LISTINGS_TEMPLATE).render(
            data={
                "records": df.to_dict("records"),
            }
        )
    )
