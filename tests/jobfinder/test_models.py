

import pytest
import pandas as pd

from jobfinder import DATA_DIR
from jobfinder.model import FoundJob
from jobfinder.utils.persistence import validate_defaults
import logging

logger = logging.getLogger(__name__)

def test_data_load():
    try:
        _jobs_file = DATA_DIR.joinpath('jobs_data.csv')
        df = pd.read_csv(_jobs_file)
        validate_defaults(df)
        for idx, row in df.iterrows():
            try:
                _found_job = FoundJob.from_dict(row.to_dict())
                logger.info(f"Found job: {idx} - {_found_job.name} \n details {_found_job.get_details()}")
                assert _found_job
            except Exception as e2:
                raise e2
    except Exception as e:
        raise e
    logger.info("PASSED")
    