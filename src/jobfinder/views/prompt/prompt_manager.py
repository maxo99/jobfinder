import streamlit as st
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
from jinja2 import Template, Environment, BaseLoader

from jobfinder.views.prompt import edit_prompt, template_builder
from jobfinder.views.prompt.helpers import save_prompt_version

# Page configuration
st.set_page_config(
    page_title="System Prompt Manager",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'prompt_history' not in st.session_state:
    st.session_state.prompt_history = []
if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt = ""
if 'saved_prompts' not in st.session_state:
    st.session_state.saved_prompts = {}
if 'template_data' not in st.session_state:
    # Sample data - replace with your actual data source
    st.session_state.template_data = pd.DataFrame({
        'instruction_id': ['inst_001', 'inst_002', 'inst_003', 'inst_004', 'inst_005'],
        'category': ['CATEGORY_1', 'CATEGORY_2', 'CATEGORY_3', 'CATEGORY_4', 'CATEGORY_5'],
        'title': ['TITLE_1', 'TITLE_2', 'TITLE_3', 'TITLE_4', 'TITLE_5'],
        'content': [
            'CONTENT_1',
            'CONTENT_2',
            'CONTENT_3',
            'CONTENT_4',
            'CONTENT_5'
        ],
        'priority': [1, 2, 3, 2, 1],
        'active': [True, True, False, True, True]
    })
if 'selected_instructions' not in st.session_state:
    st.session_state.selected_instructions = []
if 'prompt_template' not in st.session_state:
    st.session_state.prompt_template = """# System Instructions

You are an AI assistant with the following guidelines:

{% for instruction in instructions %}
## {{ instruction.category }}: {{ instruction.title }}
{{ instruction.content }}

{% endfor %}

Please follow these instructions carefully in all interactions."""




def load_prompt_from_history(version_id: str):
    """Load a prompt from history"""
    for version in st.session_state.prompt_history:
        if version['id'] == version_id:
            st.session_state.current_prompt = version['content']
            st.rerun()



def get_selected_data() -> List[Dict]:
    """Get selected instruction data as list of dictionaries"""
    if not st.session_state.selected_instructions:
        return []

    selected_df = st.session_state.template_data[
        st.session_state.template_data['instruction_id'].isin(
            st.session_state.selected_instructions)
    ]
    return selected_df.to_dict('records')




# Main UI
st.title("🤖 System Prompt Manager")
st.markdown(
    "Manage and update system prompts with version control and validation")


# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["📝 Edit Prompt", "📊 Analytics", "📚 History", "🔧 Template Builder"])

with tab1:
    edit_prompt.render()
with tab2:
    st.subheader("📊 Prompt Analytics")

    if st.session_state.prompt_history:
        # Create analytics data
        history_data = []
        for i, version in enumerate(st.session_state.prompt_history):
            history_data.append({
                'Version': f"v{len(st.session_state.prompt_history) - i}",
                'Date': datetime.fromisoformat(version['timestamp']).strftime('%Y-%m-%d %H:%M'),
                'Words': version['word_count'],
                'Characters': version['char_count'],
                'Description': version['description'] or 'No description'
            })

        # Display as dataframe
        st.dataframe(history_data, use_container_width=True)

        # Charts
        if len(history_data) > 1:
            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                st.subheader("Word Count Trend")
                st.line_chart(data=[v['word_count'] for v in reversed(
                    st.session_state.prompt_history)])

            with col_chart2:
                st.subheader("Character Count Trend")
                st.line_chart(data=[v['char_count'] for v in reversed(
                    st.session_state.prompt_history)])
    else:
        st.info(
            "No prompt versions saved yet. Save a version in the Edit tab to see analytics.")

with tab3:
    st.subheader("📚 Version History")

    if st.session_state.prompt_history:
        for i, version in enumerate(st.session_state.prompt_history):
            with st.expander(
                f"Version {len(st.session_state.prompt_history) - i} - "
                f"{datetime.fromisoformat(version['timestamp']).strftime('%Y-%m-%d %H:%M')} "
                f"({version['word_count']} words)"
            ):
                if version['description']:
                    st.markdown(f"**Description:** {version['description']}")

                col_info, col_actions = st.columns([3, 1])

                with col_info:
                    st.markdown(
                        f"**Stats:** {version['word_count']} words, {version['char_count']} characters")
                    st.markdown(f"**ID:** `{version['id']}`")

                with col_actions:
                    if st.button(f"🔄 Load This Version", key=f"load_{version['id']}"):
                        load_prompt_from_history(version['id'])
                        st.success("Version loaded!")

                # Show preview of content
                st.markdown("**Content Preview:**")
                preview = version['content'][:200]
                if len(version['content']) > 200:
                    preview += "..."
                st.text(preview)

                # Show full content in code block
                with st.expander("View Full Content"):
                    st.code(version['content'], language="text")
    else:
        st.info("No versions saved yet. Save your first version in the Edit tab!")

with tab4:
    template_builder.render(get_selected_data)
