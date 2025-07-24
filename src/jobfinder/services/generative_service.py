import logging

from jinja2 import Template

from jobfinder.adapters.chat.chat_client import ChatClient
from jobfinder.constants import (
    # SUMMARIZATION_EXAMPLE_RESPONSE,
    SUMMARIZATION_INSTRUCTIONS,
    SUMMARIZATION_LISTINGS_TEMPLATE,
)
from jobfinder.domain.models import AI, Job, ScoringResponse, SummarizationResponse
from jobfinder.utils import get_now

logger = logging.getLogger(__name__)


class GenerativeService:
    _chat_client: ChatClient

    def __init__(self, chat_client: ChatClient):
        self._chat_client = chat_client

    def generate_score(self, st, scoring_job: Job, rendered_prompt: str) -> Job | None:
        _completion = self._chat_client.completions(
            content=rendered_prompt,
            format=ScoringResponse.model_json_schema(),
        )
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

        scoring_job.score = _completion.content.get("score", 0.0)
        scoring_job.pros = _completion.content.get("pros", "N/A")
        scoring_job.cons = _completion.content.get("cons", "N/A")

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

    def extract_qualifications(self, jobs: list[Job]) -> None:
        try:
            logger.info("Extracting qualifications...")
            rendered_prompt = get_summarization_instruction_from_jobs(jobs)
            _completion = self._chat_client.completions(
                content=rendered_prompt,
                format=SummarizationResponse.model_json_schema(),
            )

            if not _completion.content:
                logger.error("No content returned from AI completion")
                raise ValueError("No content returned from AI completion")
            sr = SummarizationResponse.model_validate(_completion.content)
        except Exception as e:
            raise e

        for job in jobs:
            try:
                qualifications = sr.get_qualifications(job.id)
                if not qualifications:
                    logger.warning(f"No qualifications extracted for job ID: {job.id}")
                    continue
                job.qualifications = qualifications
                job.summarizer = AI
                job.modified = get_now()
            except Exception as e2:
                logger.error(f"Error processing job ID {job.id}: {e2}")
                continue


def get_summarization_instruction_from_jobs(jobs: list[Job]):
    _instruction = (
        SUMMARIZATION_INSTRUCTIONS
        # + SUMMARIZATION_EXAMPLE_RESPONSE
        + Template(SUMMARIZATION_LISTINGS_TEMPLATE).render(
            records=[job.model_dump() for job in jobs],
        )
    )
    return _instruction
