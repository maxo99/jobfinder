# import streamlit as st
# import pandas as pd
# from datetime import datetime

# from jobfinder.views.prompt import edit_prompt, prompt_analytics, prompt_executor
# from jobfinder.constants import PRESET_TEMPLATES

# # Page configuration
# st.set_page_config(
#     page_title="System Prompt Manager",
#     page_icon="🤖",
#     layout="wide"
# )

# # Initialize session state
# if 'prompt_history' not in st.session_state:
#     st.session_state.prompt_history = []

# if 'saved_prompts' not in st.session_state:
#     st.session_state.saved_prompts = PRESET_TEMPLATES

# if 'current_prompt' not in st.session_state:
#     st.session_state.current_prompt = next(
#         iter(st.session_state.saved_prompts.values()), ""
#     )


# if 'selected_instructions' not in st.session_state:
#     st.session_state.selected_instructions = []


# def load_prompt_from_history(version_id: str):
#     """Load a prompt from history"""
#     for version in st.session_state.prompt_history:
#         if version['id'] == version_id:
#             st.session_state.current_prompt = version['content']
#             st.rerun()


# # Main UI
# st.title("🤖 System Prompt Manager")
# st.markdown(
#     "Manage and update system prompts with version control and validation")


# # Create tabs
# tab1, tab2, tab3, tab4 = st.tabs(
#     ["📝 Edit Prompt",
#      "📊 Analytics",
#      "📚 History",
#      "🔧 Template Builder"]
#     )

# with tab1:
#     edit_prompt.render()
# with tab2:
#     prompt_analytics.render()
# with tab3:
#     st.subheader("📚 Version History")

#     if st.session_state.prompt_history:
#         for i, version in enumerate(st.session_state.prompt_history):
#             with st.expander(
#                 f"Version {len(st.session_state.prompt_history) - i} - "
#                 f"{datetime.fromisoformat(version['timestamp']).strftime('%Y-%m-%d %H:%M')} "
#                 f"({version['word_count']} words)"
#             ):
#                 if version['description']:
#                     st.markdown(f"**Description:** {version['description']}")

#                 col_info, col_actions = st.columns([3, 1])

#                 with col_info:
#                     st.markdown(
#                         f"**Stats:** {version['word_count']} words, {version['char_count']} characters")
#                     st.markdown(f"**ID:** `{version['id']}`")

#                 with col_actions:
#                     if st.button(f"🔄 Load This Version", key=f"load_{version['id']}"):
#                         load_prompt_from_history(version['id'])
#                         st.success("Version loaded!")

#                 # Show preview of content
#                 st.markdown("**Content Preview:**")
#                 preview = version['content'][:200]
#                 if len(version['content']) > 200:
#                     preview += "..."
#                 st.text(preview)

#                 # Show full content in code block
#                 with st.expander("View Full Content"):
#                     st.code(version['content'], language="text")
#     else:
#         st.info("No versions saved yet. Save your first version in the Edit tab!")

# with tab4:
#     prompt_executor.render()
