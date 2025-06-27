import logging
from jobfinder import get_filtered_jobs_df, get_jobs_df, get_session, get_status_filter, get_title_filters, set_filtered_jobs_df, set_status_filter, set_title_filters, st, update_jobs_df
from jobfinder.model import DEFAULT_STATUS_FILTERS, STATUS_OPTIONS, Status


logger = logging.getLogger(__name__)


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
    logger.info("Rendering Listings Overview")
    
    st.subheader("Records Filters")
    
    _col_1, _col_2 = st.columns(2)
    with _col_1:
    
        # _status_select = st.container(key='status_select')
        # with _status_select:
        _selected_status = st.multiselect(
            "Status",
            options=STATUS_OPTIONS,
            default=DEFAULT_STATUS_FILTERS,
        )
        if _selected_status != DEFAULT_STATUS_FILTERS:
            set_status_filter(_selected_status)
        if st.button("Reset Status Filters"):
            set_status_filter(DEFAULT_STATUS_FILTERS)

    with _col_2:
        # _titles_input = st.container(key='titles_input')
        # with _titles_input:
        new_titles = st.text_input(
            "Titles Filter (comma-separated)",
            placeholder="Enter titles to filter by, e.g. 'Software Engineer, Data Scientist'",
        )
        if new_titles:
            new_titles = [t.strip() for t in new_titles.split(',')]
            set_title_filters([*get_title_filters(), *new_titles])

        if st.button("Clear Title Filters"):
            set_title_filters([])
            st.success("Title filters cleared!")
        st.write(f"Current Title Filters:{get_title_filters()}")
        

    # Apply filters
    filtered_df = get_filtered_jobs_df()
    if _col_1:
        filtered_df = filtered_df[filtered_df['status'].isin(get_status_filter())]
    if _col_2:
        filtered_df = filtered_df[filtered_df['title'].str.contains(            '|'.join(get_title_filters()), case=False, na=False)]
        



    with st.container(key='group_operations'):

        _save_changes, _col_refresh = st.columns(2)
        with _save_changes:
            if st.button("Save Changes"):
            # Update the original dataframe with the changes
                update_jobs_df(filtered_df)
                st.success("Changes saved successfully!")
                logger.info("Changes saved successfully!")
                st.rerun()
        with _col_refresh:
            if st.button("🔄 Refresh Data"):
                set_status_filter(DEFAULT_STATUS_FILTERS)   
                set_title_filters([])
                set_filtered_jobs_df(get_jobs_df().copy())
                st.rerun()
        _group_operations(filtered_df)

    _display_stats()


    _display_columns = st.multiselect(
        "Display Columns",
        options=[*JOBSPY_COLS, *CUSTOM_COLS],
        default=[*JOBSPY_COLS, *CUSTOM_COLS],
    )

    # Display dataframe
    if not filtered_df.empty:

        st.dataframe(
            data=filtered_df[[*DEFAULT_COLS, *_display_columns]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No jobs match the current filters.")


def _group_operations(filtered_df):
    st.subheader("Group Operations")

    _set_status, _set_pros, = st.columns(2)
    _set_status.add_rows
    with _set_status:
        new_status = st.selectbox("Select Status", options=STATUS_OPTIONS)
        if st.button("Set Status"):
            filtered_df['status'] = new_status
            st.success(f"Status updated to {new_status} for selected jobs.")


    with _set_pros:
        new_pros = st.text_area("Enter Pros")
        if st.button("Set Pros"):
            filtered_df['pros'] = new_pros
            st.success(f"Pros updated for selected jobs.")


    _set_score, _set_cons = st.columns(2)
    with _set_score:
        new_score = st.number_input(
            "Score (0.0 - 10.0)",
            value=float(5.0),
            min_value=float(0),
            max_value=float(10),
            key=f"bulk_set_score"
        )

        if st.button("Set Score"):
            filtered_df['score'] = new_score
            st.success(f"Score updated to {new_score} for selected jobs.")

    with _set_cons:
        new_cons = st.text_area("Enter Cons")
        if st.button("Set Cons"):
            filtered_df['cons'] = new_cons
            st.success(f"Cons updated for selected jobs.")
            
    set_filtered_jobs_df(filtered_df)
        


def _display_stats():

    total_jobs = len(get_jobs_df())

    # FIXME: Fix for status
    # viewed_jobs = len(get_jobs_df()[get_jobs_df()['viewed'] == True])
    # unviewed_jobs = total_jobs - viewed_jobs

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs", total_jobs)
    # col2.metric("Viewed Jobs", viewed_jobs)
    # col3.metric("Unviewed Jobs", unviewed_jobs)
