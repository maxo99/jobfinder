import os
from streamlit.testing.v1 import AppTest
from jobfinder import RAW_DATA_DIR
from jobfinder.session import get_jobs_df, _init_session


def test_find_jobs():
    try:
        at = AppTest.from_file("main.py", default_timeout=30).run(timeout=60)
        _init_session()
        _starting_raw_count = len(os.listdir(RAW_DATA_DIR))
        at.button(key="scrape_job").click().run()
        data = get_jobs_df()
        assert _starting_raw_count < len(os.listdir(RAW_DATA_DIR))
        assert not data.empty

    except Exception as e:
        print(f"Error occurred: {e}")
        raise e


# def test_scoring_util():
#     try:
#         at = AppTest.from_file("main.py", default_timeout=30).run(timeout=60)
#         _init_session()
#         # Ensure we have some jobs to score
#         data = get_jobs_df()
#         assert not data.empty, "No jobs available for scoring."

#         # Navigate to the scoring tab
#         # at.button(key="scoring_util").click().run()

#         selected_indices = [1, 2]
#         set_selected_data([data.iloc[i]["id"] for i in selected_indices])


#         # # Select a job for scoring
#         # at.selectbox(
#         #     key="select_listing_scoring",
#         #     options=list(data.index),
#         #     index=0  # Select the first job by default
#         # ).run()

#         # Check if the scoring template is loaded
#         # assert "current_prompt" in at.session_state, "Scoring prompt not loaded."

#         # Generate score button should be present
#         at.button(
#             "Generate Score",
#         ).click().run()

#     except Exception as e:
#         print(f"Error occurred in scoring util test: {e}")
#         raise e
