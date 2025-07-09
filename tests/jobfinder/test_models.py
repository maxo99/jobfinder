

import pandas as pd
from jobfinder import DATA_DIR
from jobfinder.model import validate_defaults,found_jobs_from_df
import logging

from jobfinder.views.summarization_util import summarize_jobs

logger = logging.getLogger(__name__)

def test_data_load():
    try:
        _jobs_file = DATA_DIR.joinpath('jobs_data.csv')
        df = pd.read_csv(_jobs_file)
        validate_defaults(df)
        
        _found_jobs = found_jobs_from_df(df)
        converted_df = pd.DataFrame([job.model_dump() for job in _found_jobs.values()])
        assert not converted_df.empty
        
    except Exception as e:
        raise e
    logger.info("PASSED")
    
    
    
def test_summarization_util():
    

    try:
        _jobs_file = DATA_DIR.joinpath('jobs_data.csv')
        df = pd.read_csv(_jobs_file)
        validate_defaults(df)

        # Test summarization with a small subset of jobs
        sample_df = df.head(1)
        summarize_jobs(sample_df)
        assert sample_df['summary'].notnull().all(), "Summarization failed for some jobs."
        print("Finished")

    except Exception as e:
        raise e
    logger.info("PASSED")