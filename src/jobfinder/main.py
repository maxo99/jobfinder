import logging

import streamlit as st
from streamlit import session_state as ss

from jobfinder import _setup_logging
from jobfinder.domain.constants import DEFAULT_PAGE_DESCRIPTION
from jobfinder.pages import listings_overview
from jobfinder.session import (
    _init_session,
    _init_working_df,
    get_working_df,
)
from jobfinder.views import common

logger = logging.getLogger(__name__)


def main():
    logging.info("Starting up main()")
    st.set_page_config(
        page_title="jobfinder",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    if "initialized" not in ss:
        _setup_logging()
        _init_session()
    _init_working_df()

    common.render_header()
    if not get_working_df().empty:
        listings_overview.render(st)
    else:
        st.info("Configure your job search and start scraping.")
        st.markdown(DEFAULT_PAGE_DESCRIPTION)
    common.render_footer()


if __name__ == "__main__":
    main()
