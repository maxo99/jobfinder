import os
import logging
from typing import Literal
import pandas as pd
from jobfinder import RAW_DATA_DIR, st, JOBS_DATA_FILE
from jobfinder.model import UserType, Status
from jobfinder.utils import get_now

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


def update_results(new_jobs):
    # Remove duplicates based on job_url or title+company
    df = pd.concat([st.session_state.jobs_df, new_jobs], ignore_index=True)

    df = handle_duplicates(df)
    st.session_state.jobs_df = df


def handle_duplicates(df):
    #  TODO: UPDATE DUPLICATE HANDLING LOGIC
    # Remove duplicates based on job_url or title+company
    if "job_url" in df.columns:
        df = df.drop_duplicates(subset=["job_url"], keep="last")
    else:
        df = df.drop_duplicates(subset=["title", "company"], keep="last")
    return df



def save_data2(df: pd.DataFrame, state: Literal["raw", "processed"] = "processed"):
    try:
        if state == "processed":
            _data_file = JOBS_DATA_FILE
        else:
            _data_file = os.path.join(RAW_DATA_DIR, f"jobs_data_{get_now()}.csv")
        df.to_csv(_data_file, index=False)
        logger.info(f"Data saved to {_data_file}")
        st.success("Data saved successfully!")
    except Exception as e:
        st.error(f"Error saving data: {e}")


def validate_defaults(df):
    if "date_scraped" not in df.columns:
        df["date_scraped"] = get_now()
    if "modified" not in df.columns:
        df["modified"] = get_now()
    if "status" not in df.columns:
        df["status"] = Status.NEW.value
    if "pros" not in df.columns:
        df["pros"] = ""
    if "cons" not in df.columns:
        df["cons"] = ""
    if "score" not in df.columns:
        df["score"] = None
    if "summary" not in df.columns:
        df["summary"] = None
    if "classifier" not in df.columns:
        df["classifier"] = UserType.NA.value
    if "summarizer" not in df.columns:
        df["summarizer"] = UserType.NA.value
    df["date_posted"] = df["date_posted"].astype(str)
