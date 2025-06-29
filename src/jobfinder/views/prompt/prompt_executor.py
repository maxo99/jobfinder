# import streamlit as st
# from typing import Dict
# from jinja2 import Template

# from jobfinder.constants import TEMPLATE_HELP_MD
# from jobfinder.views.prompt.helpers import get_selected_data


# def render():
#     st.subheader("🔧 Prompt Executor")

#     st.markdown(
#         "Select instructions from the data table and generate system prompts using Jinja2 templates"
#     )


#     col_data, col_template = st.columns([1, 1])

#     with col_data:
#         st.subheader("📊 Available Instructions")

#         # Display and selection
#         df_display = st.session_state.template_data.copy()

#         # Selection interface
#         st.markdown("**Select Instructions:**")
#         selection_mode = st.radio(
#             "Selection Mode",
#             ["Individual Selection", "Bulk Selection"],
#             horizontal=True
#         )

#         if selection_mode == "Individual Selection":
#             # Individual checkboxes
#             selected_ids = []
#             for idx, row in df_display.iterrows():
#                 status_icon = "✅" if row['active'] else "❌"
#                 priority_stars = "⭐" * row['priority']

#                 is_selected = st.checkbox(
#                     f"{status_icon} [{row['category']}] {row['title']} {priority_stars}",
#                     key=f"select_{row['instruction_id']}",
#                     value=row['instruction_id'] in st.session_state.selected_instructions
#                 )

#                 if is_selected:
#                     selected_ids.append(row['instruction_id'])

#                 with st.expander(f"Preview: {row['title']}"):
#                     st.write(f"**ID:** {row['instruction_id']}")
#                     st.write(f"**Content:** {row['content']}")

#             st.session_state.selected_instructions = selected_ids

#         else:
#             # Bulk selection with dataframe
#             st.markdown("**Select rows by clicking on them:**")

#             # Create selection dataframe
#             selection_df = df_display[[
#                 'instruction_id', 'category', 'title', 'priority', 'active']].copy()

#             selected_rows = st.dataframe(
#                 selection_df,
#                 use_container_width=True,
#                 on_select="rerun",
#                 selection_mode="multi-row"
#             )

#             if selected_rows and 'selection' in selected_rows and 'rows' in selected_rows['selection']:
#                 selected_indices = selected_rows['selection']['rows']
#                 st.session_state.selected_instructions = [
#                     selection_df.iloc[i]['instruction_id'] for i in selected_indices
#                 ]

#         # Show selected count
#         st.info(
#             f"📋 Selected {len(st.session_state.selected_instructions)} instructions")

#         # Quick actions
#         quick_col1, quick_col2, quick_col3 = st.columns(3)
#         with quick_col1:
#             if st.button("🔄 Select All Active", use_container_width=True):
#                 active_ids = df_display[df_display['active']
#                                         == True]['instruction_id'].tolist()
#                 st.session_state.selected_instructions = active_ids
#                 st.rerun()

#         with quick_col2:
#             if st.button("⭐ Select High Priority", use_container_width=True):
#                 high_priority_ids = df_display[df_display['priority']
#                                                >= 3]['instruction_id'].tolist()
#                 st.session_state.selected_instructions = high_priority_ids
#                 st.rerun()

#         with quick_col3:
#             if st.button("🗑️ Clear Selection", use_container_width=True):
#                 st.session_state.selected_instructions = []
#                 st.rerun()

#     with col_template:

#         st.subheader("👀 Template Preview")

#         if st.session_state.selected_instructions:
#             # Get selected data
#             selected_data = get_selected_data()

#             # Render template
#             rendered_prompt = _render_jinja(
#                 st.session_state.current_prompt,
#                 {'instructions': selected_data}
#             )

#             # Show preview
#             st.code(rendered_prompt, language="markdown")

#             if st.button("📋 Use for run", use_container_width=True):
#                 st.markdown("Not yet implemented")

#         else:
#             st.info("Select instructions from the left panel to see template preview")


# def _render_jinja(template_str: str, data: Dict) -> str:
#     """Render Jinja2 template with provided data"""
#     try:
#         template = Template(template_str)
#         return template.render(**data)
#     except Exception as e:
#         return f"Template Error: {str(e)}"
