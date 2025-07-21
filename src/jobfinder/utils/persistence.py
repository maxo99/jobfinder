import logging
import os
from typing import Literal

import pandas as pd

from jobfinder import JOBS_DATA_FILE, RAW_DATA_DIR
from jobfinder.utils import get_now

logger = logging.getLogger(__name__)


# def update_results(new_jobs):
#     validate_defaults(new_jobs)
#     df = pd.concat([get_jobs_df(), new_jobs], ignore_index=True)
#     df = handle_duplicates(df)
#     set_jobs_df(df)
#     save_data2(df, state="processed")


# def handle_duplicates(df):
#     #  TODO: UPDATE DUPLICATE HANDLING LOGIC
#     # Remove duplicates based on job_url or title+company
#     if "job_url" in df.columns:
#         # Log duplicates before dropping them
#         duplicates = df[df.duplicated(subset=["job_url"], keep=False)]
#         if not duplicates.empty:
#             logger.info(f"Found {len(duplicates)} job_url duplicate")
#             _log_duplicates(duplicates)
#         df = df.drop_duplicates(subset=["job_url"], keep="last")

#     else:
#         # Log duplicates before dropping them
#         duplicates = df[df.duplicated(subset=["title", "company"], keep=False)]
#         if not duplicates.empty:
#             logger.info(f"Found {len(duplicates)} title+company duplicate")
#             _log_duplicates(duplicates)

#         df = df.drop_duplicates(subset=["title", "company"], keep="last")
#     return df


# def _log_duplicates(df):
#     for _, j in df.iterrows():
#         logger.debug(
#             f"Duplicate: {j.get('title', 'N/A')} at {j.get('company', 'N/A')}"
#             )


def save_data2(df: pd.DataFrame, state: Literal["raw", "processed"] = "processed"):
    try:
        if state == "processed":
            _data_file = JOBS_DATA_FILE
        else:
            _data_file = os.path.join(RAW_DATA_DIR, f"jobs_data_{get_now()}.csv")
        df.to_csv(_data_file, index=False)
        logger.info(f"Data saved to {_data_file}")
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise e
