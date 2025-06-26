from jobfinder import get_jobs_df, get_session, st
from jobfinder.model import Status

DEFAULT_COLS = [
    'date_posted',
    'site',
    'company',
    'title',
]

JOBSPY_COLS = [

    # 'id',
    # 'job_url',
    # 'job_url_direct',

    # 'location',
    'is_remote',
    'job_type',

    # Salary
    # 'salary_source',
    # 'interval',
    # 'min_amount',
    # 'max_amount',
    # 'currency',
    # 'job_level',
    # 'job_function',
    # 'description',
    # 'company_industry',
    # 'company_url',
    # 'listing_type',
    # 'emails',
    # 'company_logo',
    # 'company_url_direct',
    # 'company_addresses',
    # 'company_num_employees',
    # 'company_revenue',
    # 'company_description',
    # 'skills',
    # 'experience_range',
    # 'company_rating',
    # 'company_reviews_count',
    # 'vacancy_count',
    # 'work_from_home_type'
]
CUSTOM_COLS = [
    'status',
    'score',
    'pros',
    'cons',
]
DISPLAY_COLS = [*DEFAULT_COLS, *JOBSPY_COLS, *CUSTOM_COLS]


def render():
    
    _display_stats()
    
    _col_status_select, _col_display_columns, _col_refresh = st.columns(3)
    with _col_status_select:
        _selected_status = st.multiselect(
            "Status",
            options=[s.value for s in Status],
            default=[s.value for s in Status if s != Status.EXCLUDED],
        )
    with _col_display_columns:
         # TODO: Update default display cols
        _display_columns = st.multiselect(
            "Display Columns",
            options=DISPLAY_COLS,
            default=DISPLAY_COLS,
        )
    with _col_refresh:
        if st.button("🔄 Refresh Data"):
            st.rerun()


    # Apply filters
    filtered_df = get_jobs_df().copy()
    if _col_status_select:
        filtered_df = filtered_df[filtered_df['status'].isin(_selected_status)]

    # Display dataframe
    if not filtered_df.empty:
        
        # TODO: Select columns to display

        st.dataframe(
            data=filtered_df[_display_columns],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No jobs match the current filters.")


def _display_stats():
    
    total_jobs = len(get_jobs_df())
    
    
    # FIXME: Fix for status
    # viewed_jobs = len(get_jobs_df()[get_jobs_df()['viewed'] == True])
    # unviewed_jobs = total_jobs - viewed_jobs

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs", total_jobs)
    # col2.metric("Viewed Jobs", viewed_jobs)
    # col3.metric("Unviewed Jobs", unviewed_jobs)