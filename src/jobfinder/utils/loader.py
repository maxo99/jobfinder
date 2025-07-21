import logging
import os
from typing import Literal

import numpy as np
import pandas as pd

from jobfinder import JOBS_DATA_FILE, RAW_DATA_DIR
from jobfinder.domain.models import Job, df_to_jobs, validate_df_defaults

logger = logging.getLogger(__name__)


def load_raw_jobs_df(state: Literal["raw", "processed"] = "processed") -> pd.DataFrame:
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
                temp_df = pd.read_csv(csv_file).replace({np.nan: None})
                dfs.append(temp_df)
            df = pd.concat(dfs, ignore_index=True)
        else:
            df = pd.DataFrame()
        validate_df_defaults(df)
        logger.info(f"Loaded {len(df)} records from raw data.")
        return df
    except Exception as e:
        logger.warning(f"Error loading existing data: {e}")
        return pd.DataFrame()


def load_raw_jobs(_input: pd.DataFrame | None = None) -> list[Job]:
    if _input is None:
        _input = load_raw_jobs_df()
    return df_to_jobs(_input)


# def load_data2(state: Literal["raw", "processed"] = "processed"):
#     logger.info(f"Loading data with state: {state}")
#     _data_files = []
#     if state == "processed":
#         _data_files = [JOBS_DATA_FILE]
#     else:
#         _data_files = [
#             os.path.join(RAW_DATA_DIR, f)
#             for f in os.listdir(RAW_DATA_DIR)
#             if f.endswith(".csv")
#         ]
#     try:
#         if _data_files:
#             dfs = []
#             for csv_file in _data_files:
#                 temp_df = pd.read_csv(csv_file).replace({np.nan: None})
#                 dfs.append(temp_df)
#             df = pd.concat(dfs, ignore_index=True)
#         else:
#             df = pd.DataFrame()
#         validate_defaults(df)
#         return df
#     except Exception as e:
#         logger.warning(f"Error loading existing data: {e}")
#         return pd.DataFrame()
