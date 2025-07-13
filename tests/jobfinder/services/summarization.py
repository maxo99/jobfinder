import logging
from jobfinder.services.summarization_service import summarize_jobs
from jobfinder.session import get_jobs_df

logger = logging.getLogger(__name__)

def test_summarization_util(mock_get_jobs_df, mock_openai_client_summarizer):

    try:
        sample_df = get_jobs_df().head(2)
        summarize_jobs(mock_openai_client_summarizer, sample_df, False)
        assert sample_df['summary'].notnull().all(), "Summarization failed for some jobs."
        print("Finished")

    except Exception as e:
        raise e
    logger.info("PASSED")