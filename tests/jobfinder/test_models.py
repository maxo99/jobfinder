

import pandas as pd
from jobfinder.model import found_jobs_from_df
import logging

from jobfinder.views.summarization_util import summarize_jobs

logger = logging.getLogger(__name__)

def test_data_load(fix_jobs_data):
    try:
        _input_data = fix_jobs_data.copy()
        _found_jobs = found_jobs_from_df(_input_data)
        converted_df = pd.DataFrame([job.model_dump() for job in _found_jobs.values()])
        assert not converted_df.empty
        _input_data = pd.concat([_input_data, converted_df], ignore_index=True)

    except Exception as e:
        raise e
    logger.info("PASSED")
    
    
    

def test_summarization_util(fix_jobs_data,mock_openai_client):
    
    try:

        # Test summarization with a small subset of jobs
        sample_df = fix_jobs_data.head(1)
        summarize_jobs(sample_df)
        assert sample_df['summary'].notnull().all(), "Summarization failed for some jobs."
        print("Finished")

    except Exception as e:
        raise e
    logger.info("PASSED")