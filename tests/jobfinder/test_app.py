import os
from streamlit.testing.v1 import AppTest

from jobfinder import RAW_DATA_DIR, get_jobs_df
from main import _init_session

def test_find_jobs():
    try:
        """A user increments the number input, then clicks Add"""
        at = AppTest.from_file("main.py",default_timeout=30).run(timeout=60)
        _init_session()
        _starting_raw_count = len(os.listdir(RAW_DATA_DIR))
        # at.button(key="main_tabs").click().run()  # Click on the first tab (Job Overview)
        at.button(key="scrape_job").click().run()  # Click on the Scr
        data = get_jobs_df()
        assert _starting_raw_count < len(os.listdir(RAW_DATA_DIR)), "No new raw data files created."
        assert not data.empty
        
    except Exception as e:
        print(f"Error occurred: {e}")
        raise e
