

import pandas as pd
from jobfinder.model import found_jobs_from_df
import logging

from jobfinder.utils.loader import load_data2


logger = logging.getLogger(__name__)

def test_data_serialization():
    try:
        
        _input_data = load_data2(state="processed").copy()
        _found_jobs = found_jobs_from_df(_input_data)
        converted_df = pd.DataFrame([job.model_dump() for job in _found_jobs.values()])
        assert not converted_df.empty
        _input_data = pd.concat([_input_data, converted_df], ignore_index=True)

    except Exception as e:
        raise e
    logger.info("PASSED")
    
    
    
