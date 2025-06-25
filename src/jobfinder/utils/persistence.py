import pandas as pd
import os
from jobfinder import st
from jobfinder.utils import get_now


def load_existing_data():
    if os.path.exists(st.session_state.job_data_file):
        try:
            df = pd.read_csv(st.session_state.job_data_file)
            validate_defaults(df)
            return df
        except Exception as e:
            st.error(f"Error loading existing data: {e}")
            return pd.DataFrame()
    return pd.DataFrame()


def update_results(new_jobs):
    # Remove duplicates based on job_url or title+company
    df = pd.concat([st.session_state.jobs_df, new_jobs], ignore_index=True)

    # TODO: Handle Duplicates
    if 'job_url' in df.columns:
        df = df.drop_duplicates(subset=['job_url'], keep='last')
    else:
        df = df.drop_duplicates(subset=['title', 'company'], keep='last')

    st.session_state.jobs_df = df


def save_data(df):
    try:
        df.to_csv(st.session_state.job_data_file, index=False)
        st.success("Data saved successfully!")
    except Exception as e:
        st.error(f"Error saving data: {e}")


def validate_defaults(df):
    if 'date_scraped' not in df.columns:
        df['date_scraped'] = get_now()
    if 'viewed' not in df.columns:
        df['viewed'] = False
    if 'pros' not in df.columns:
        df['pros'] = ''
    if 'cons' not in df.columns:
        df['cons'] = ''
    if 'score' not in df.columns:
        df['score'] = ''
