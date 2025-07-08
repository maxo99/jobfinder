import logging
import os
from typing import Literal

import pandas as pd

from jobfinder import JOBS_DATA_FILE, RAW_DATA_DIR
from jobfinder.model import validate_defaults

logger = logging.getLogger(__name__)


def load_data2(state: Literal["raw", "processed"] = "processed"):
    logger.info(f"Loading data with state: {state}")
    _data_files = []
    if state == "processed":
        _data_files = [JOBS_DATA_FILE]
    else:
        _data_files = [
            os.path.join(RAW_DATA_DIR, f)
            for f in os.listdir(RAW_DATA_DIR)
            if f.endswith(".csv")
        ]
    try:
        if _data_files:
            dfs = []
            for csv_file in _data_files:
                temp_df = pd.read_csv(csv_file)
                dfs.append(temp_df)
            df = pd.concat(dfs, ignore_index=True)
        else:
            df = pd.DataFrame()
        validate_defaults(df)
        return df
    except Exception as e:
        logger.warning(f"Error loading existing data: {e}")
        return pd.DataFrame()
