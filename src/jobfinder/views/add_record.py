import logging
import pandas as pd
from jobfinder.model import Classifier
from jobfinder.utils import get_now
from jobfinder.utils.persistence import save_data, update_results
from jobfinder import get_jobs_df, st

logger = logging.getLogger(__name__)


def render():
    with st.form("my_form"):
        st.write("Manually create records to use for scoring context.")
        title = st.text_area("title")
        pros = st.text_area("pros")
        cons = st.text_area("cons")
        score = st.number_input(
            "Score (0.0 - 10.0)",
            value=5.0,
            min_value=float(0),
            max_value=float(10),
            key="score_new_job",
        )
        submit = st.form_submit_button("Submit")
        if submit:
            st.text("Submitted")

            _new_record = pd.DataFrame(
                {
                    "id": [f"USER_CLASSIFIED_{get_now()}"],
                    "company": ["USER_ADDED"],
                    "title": [title],
                    "pros": [pros],
                    "cons": [cons],
                    "score": [score],
                    "classifier": [Classifier.USER.value],
                    "modified": [get_now()],
                },
            )
            update_results(_new_record)
            save_data(get_jobs_df())
            st.success("Record added successfully!")
            st.rerun()
