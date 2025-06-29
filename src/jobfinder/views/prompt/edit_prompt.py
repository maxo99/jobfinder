
# import streamlit as st

# from jobfinder.constants import TEMPLATE_HELP_MD
# from jobfinder.views.prompt.helpers import save_prompt_version, validate_prompt


# def render():
    
    
#     with st.expander("📖 Template Help & Variables"):

#         st.markdown(TEMPLATE_HELP_MD)
    
#     col1, col2 = st.columns([2, 1])

#     with col1:
#         st.subheader("Current System Prompt")

#         # Text area for prompt editing
#         prompt_text = st.text_area(
#             "System Prompt Content",
#             value=st.session_state.current_prompt,
#             height=400,
#             help="Enter or modify your system prompt here",
#             key="prompt_editor"
#         )

#         # Update current prompt
#         st.session_state.current_prompt = prompt_text

#         # Action buttons
#         col_load, col_save = st.columns(2)

#         with col_load:

#             selected_preset = st.selectbox(
#                 "Choose a preset template:",
#                 list(st.session_state.saved_prompts.keys())
#             )

#             if st.button("📥 Load Preset", use_container_width=True):
#                 st.session_state.current_prompt = st.session_state.saved_prompts[selected_preset]
#                 st.rerun()

#             if st.button("🗑️ Clear", use_container_width=True):
#                 st.session_state.current_prompt = ""
#                 st.rerun()

#         with col_save:
#             description = st.text_input(
#                 "Version Description (optional)",
#                 placeholder="e.g., Added new instructions for..."
#             )
#             if st.button("💾 Save Version", use_container_width=True):
#                 if save_prompt_version(prompt_text, description):
#                     st.success("✅ Version saved successfully!")
#                 else:
#                     st.info("ℹ️ This prompt version already exists")








#     with col2:
#         st.subheader("Validation & Stats")

#         # Validate current prompt
#         validation = validate_prompt(prompt_text)

#         # Display validation status
#         if validation['is_valid']:
#             st.success("✅ Prompt is valid")
#         else:
#             st.error("❌ Prompt has issues")

#         # Display warnings
#         if validation['warnings']:
#             st.warning("⚠️ Warnings:")
#             for warning in validation['warnings']:
#                 st.write(f"• {warning}")

#         # Display stats
#         st.subheader("📊 Statistics")
#         stats = validation['stats']

#         col_stat1, col_stat2 = st.columns(2)
#         with col_stat1:
#             st.metric("Words", stats['word_count'])
#             st.metric("Lines", stats['line_count'])

#         with col_stat2:
#             st.metric("Characters", stats['char_count'])
#             st.metric("Paragraphs", stats['paragraph_count'])

