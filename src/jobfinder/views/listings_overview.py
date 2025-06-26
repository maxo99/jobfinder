from jobfinder import st


JOBSPY_COLS = [
    'title',
    'company',
    'date_posted',

    'id',
    'site',
    'job_url',
    'job_url_direct',

    'location',
    'is_remote',
    'job_type',

    # Salary
    'salary_source',
    'interval',
    'min_amount',
    'max_amount',
    'currency',

    'job_level',
    'job_function',

    'description',
    'company_industry',
    'company_url',
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
    'viewed',
    'pros',
    'cons',
    'score',
]
DISPLAY_COLS = [*JOBSPY_COLS, *CUSTOM_COLS]


def render():
    # Filter controls
    col1, col2, col3 = st.columns(3)
    with col1:
        show_viewed = st.checkbox("Show Viewed Jobs", value=True)
    with col2:
        show_unviewed = st.checkbox("Show Unviewed Jobs", value=True)
    with col3:
        if st.button("🔄 Refresh Data"):
            st.rerun()

    # Apply filters
    filtered_df = st.session_state.jobs_df.copy()
    if not show_viewed:
        filtered_df = filtered_df[filtered_df['viewed'] == False]
    if not show_unviewed:
        filtered_df = filtered_df[filtered_df['viewed'] == True]

    # Display stats
    total_jobs = len(st.session_state.jobs_df)
    viewed_jobs = len(
        st.session_state.jobs_df[st.session_state.jobs_df['viewed'] == True])
    unviewed_jobs = total_jobs - viewed_jobs

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs", total_jobs)
    col2.metric("Viewed Jobs", viewed_jobs)
    col3.metric("Unviewed Jobs", unviewed_jobs)

    # Display dataframe
    if not filtered_df.empty:
        # Select columns to display

        available_columns = [
            col for col in DISPLAY_COLS if col in filtered_df.columns
        ]

        st.dataframe(
            filtered_df[available_columns],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No jobs match the current filters.")
