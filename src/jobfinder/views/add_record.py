import logging
import pandas as pd
from jobfinder.model import UserType
from jobfinder.utils import get_now
from jobfinder.utils.persistence import save_data2, update_results
from jobfinder.session import get_jobs_df, st

logger = logging.getLogger(__name__)


def render():
    with st.form("my_form"):
        st.write("Manually create records to use for scoring context.")
        title = st.text_area("title")
        summary = st.text_area("summary")
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

            if summary:
                _summarizer = UserType.USER.value
            else:
                _summarizer = UserType.NA.value

            if pros or cons or score is not None:
                _classifier = UserType.USER.value
            else:
                _classifier = UserType.NA.value

            _new_record = pd.DataFrame(
                {
                    "id": [f"USER_CREATED_{get_now()}"],
                    "company": ["USER_ADDED"],
                    "title": [title],
                    "pros": [pros],
                    "summary": [summary],
                    "cons": [cons],
                    "score": [score],
                    "classifier": [_classifier],
                    "summarizer": [_summarizer],
                    "modified": [get_now()],
                },
            )
            update_results(_new_record)
            save_data2(get_jobs_df())
            st.success("Record added successfully!")
            st.rerun()
