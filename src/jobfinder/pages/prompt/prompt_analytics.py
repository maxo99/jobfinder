import streamlit as st
from datetime import datetime


def _render_history_chart():
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Word Count Trend")
        st.line_chart(
            data=[v["word_count"] for v in reversed(st.session_state.prompt_history)]
        )

    with col_chart2:
        st.subheader("Character Count Trend")
        st.line_chart(
            data=[v["char_count"] for v in reversed(st.session_state.prompt_history)]
        )


def render():
    st.subheader("📊 Prompt Analytics")

    if st.session_state.prompt_history:
        # Create analytics data
        history_data = []
        for i, version in enumerate(st.session_state.prompt_history):
            history_data.append(
                {
                    "Version": f"v{len(st.session_state.prompt_history) - i}",
                    "Date": datetime.fromisoformat(version["timestamp"]).strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "Words": version["word_count"],
                    "Characters": version["char_count"],
                    "Description": version["description"] or "No description",
                }
            )

        # Display as dataframe
        st.dataframe(history_data, use_container_width=True)

        # Charts
        if len(history_data) > 1:
            _render_history_chart()
    else:
        st.info(
            "No prompt versions saved yet. Save a version in the Edit tab to see analytics."
        )
