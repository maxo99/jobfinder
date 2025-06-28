



from jobfinder import st, get_jobs_df


def render():

    if not get_jobs_df().empty:
        st.subheader("Scoring Utility")
        st.markdown(
            """
            This section is intended to provide tools and utilities for scoring and evaluating job listings.
            """
        )
        
    
        