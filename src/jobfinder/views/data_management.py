import os
from pandas import DataFrame
from jobfinder import st
from jobfinder.utils import get_now
from jobfinder.utils.persistence import save_data



def render():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Export Data")
        if st.button("📥 Download CSV"):
            csv_data = st.session_state.jobs_df.to_csv(index=False)
            st.download_button(
                label="Download jobs data as CSV",
                data=csv_data,
                file_name=f"jobs_export_{get_now(underscore=True)}.csv",
                mime="text/csv"
            )

    with col2:
        st.subheader("Clear Data")
        if st.button("🗑️ Clear All Data", type="secondary"):
            if st.button("⚠️ Confirm Clear All", key="confirm_clear"):
                st.session_state.jobs_df = DataFrame()
                if os.path.exists(st.session_state.job_data_file):
                    os.remove(st.session_state.job_data_file)
                    print(f"Cleared : {st.session_state.job_data_file}")
                else:
                    print(f"WARNING File not exists:{st.session_state.job_data_file}")
                st.success("All data cleared!")
                st.rerun()

    # Data file management
    st.subheader("Data File")
    st.write(f"Current data file: `{st.session_state.job_data_file}`")

    # Bulk actions
    st.subheader("Bulk Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Mark All as Viewed"):
            st.session_state.jobs_df['viewed'] = True
            save_data(st.session_state.jobs_df)
            st.success("All jobs marked as viewed!")
            st.rerun()

    with col2:
        if st.button("Mark All as Unviewed"):
            st.session_state.jobs_df['viewed'] = False
            save_data(st.session_state.jobs_df)
            st.success("All jobs marked as unviewed!")
            st.rerun()