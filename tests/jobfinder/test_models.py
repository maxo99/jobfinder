

import pytest
import pandas as pd
from jobfinder import DATA_DIR
from jobfinder.model import validate_defaults,found_jobs_from_df
import logging

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
    