

import pytest
import pandas as pd

from jobfinder import DATA_DIR
from jobfinder.model import FoundJob
from jobfinder.utils.persistence import validate_defaults


def test_data_load():
    try:
        _jobs_file = DATA_DIR.joinpath('jobs_data.csv')
        df = pd.read_csv(_jobs_file)
        validate_defaults(df)
        for idx, row in df.iterrows():
            try:
                _found_job = FoundJob.model_validate(row.to_dict())
            except Exception as e2:
                raise e2
    except Exception as e:
        raise e
    print("PASSED")