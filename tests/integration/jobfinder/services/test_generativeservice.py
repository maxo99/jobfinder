import logging

from jobfinder.session import get_jobs_df

logger = logging.getLogger(__name__)


# def test_summarize_jobs_mocked(mock_get_jobs_df, mock_openai_client_summarizer):
#     try:
#         sample_df = get_jobs_df().head(2)
#         summarize_jobs(mock_openai_client_summarizer, sample_df, False)
#         assert sample_df["summary"].notnull().all(), (
#             "Summarization failed for some jobs."
#         )
#         print("Finished")

#     except Exception as e:
#         raise e
#     logger.info("PASSED")


def test_summarize_jobs(raw_jobs_df, fix_generativeservice):
    try:
        sample_df = raw_jobs_df.head(2)
        fix_generativeservice.summarize_jobs(sample_df)
        assert sample_df["summary"].notnull().all(), (
            "Summarization failed for some jobs."
        )
        print("Finished")

    except Exception as e:
        raise e
    logger.info("PASSED")
