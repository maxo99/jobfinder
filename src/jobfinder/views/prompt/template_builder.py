import streamlit as st
import json
import pandas as pd
from typing import Dict, List, Optional
import hashlib
from jinja2 import Template, Environment, BaseLoader

from jobfinder.views.prompt.helpers import save_prompt_version



def render(get_selected_data):
    st.subheader("🔧 Template Builder")

    st.markdown(
        "Select instructions from the data table and generate system prompts using Jinja2 templates"
    )
    
    with st.expander("📖 Template Help & Variables"):

            st.markdown("""
            **Available Variables:**
            - `instructions`: List of selected instruction objects
            **Object Properties:**
            - `instruction.instruction_id`: Unique identifier
            - `instruction.category`: Category name
            - `instruction.title`: Instruction title
            - `instruction.content`: Instruction content
            - `instruction.priority`: Priority level (1-5)
            - `instruction.active`: Boolean active status
            **Example Templates:**
            ```jinja2
            {% for instruction in instructions %}
            ## {{ instruction.title }}
            {{ instruction.content }}
            {% endfor %}
            ```
            **Conditional Logic:**
            ```jinja2
            {% for instruction in instructions %}
            {% if instruction.priority >= 3 %}
            ⭐ HIGH PRIORITY: {{ instruction.title }}
            {% endif %}
            {{ instruction.content }}
            {% endfor %}
            ```
            """)



    # Split into columns
    col_data, col_template = st.columns([1, 1])

    with col_data:
        st.subheader("📊 Available Instructions")

        # # Data management section
        # with st.expander("🔧 Data Management"):
        #     with st.form("add_instruction"):
        #         new_id = st.text_input("Instruction ID")
        #         new_category = st.text_input("Category")
        #         new_title = st.text_input("Title")
        #         new_content = st.text_area("Content", height=100)
        #         new_priority = st.selectbox("Priority", [1, 2, 3, 4, 5])
        #         new_active = st.checkbox("Active", value=True)

        #         if st.form_submit_button("Add Instruction"):
        #             if new_id and new_category and new_title and new_content:
        #                 new_row = pd.DataFrame({
        #                     'instruction_id': [new_id],
        #                     'category': [new_category],
        #                     'title': [new_title],
        #                     'content': [new_content],
        #                     'priority': [new_priority],
        #                     'active': [new_active]
        #                 })
        #                 st.session_state.template_data = pd.concat([st.session_state.template_data, new_row], ignore_index=True)
        #                 st.success("✅ Instruction added!")
        #                 st.rerun()
        #             else:
        #                 st.error("Please fill in all required fields")

        # Display and selection
        df_display = st.session_state.template_data.copy()

        # Filters
        st.markdown("**Filters:**")
        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            category_filter = st.multiselect(
                "Filter by Category",
                options=df_display['category'].unique(),
                default=df_display['category'].unique()
            )

        with filter_col2:
            active_filter = st.selectbox(
                "Filter by Status", ["All", "Active Only", "Inactive Only"])

        # Apply filters
        if category_filter:
            df_display = df_display[df_display['category'].isin(
                category_filter)]

        if active_filter == "Active Only":
            df_display = df_display[df_display['active'] == True]
        elif active_filter == "Inactive Only":
            df_display = df_display[df_display['active'] == False]

        # Selection interface
        st.markdown("**Select Instructions:**")
        selection_mode = st.radio(
            "Selection Mode",
            ["Individual Selection", "Bulk Selection"],
            horizontal=True
        )

        if selection_mode == "Individual Selection":
            # Individual checkboxes
            selected_ids = []
            for idx, row in df_display.iterrows():
                status_icon = "✅" if row['active'] else "❌"
                priority_stars = "⭐" * row['priority']

                is_selected = st.checkbox(
                    f"{status_icon} [{row['category']}] {row['title']} {priority_stars}",
                    key=f"select_{row['instruction_id']}",
                    value=row['instruction_id'] in st.session_state.selected_instructions
                )

                if is_selected:
                    selected_ids.append(row['instruction_id'])

                with st.expander(f"Preview: {row['title']}"):
                    st.write(f"**ID:** {row['instruction_id']}")
                    st.write(f"**Content:** {row['content']}")

            st.session_state.selected_instructions = selected_ids

        else:
            # Bulk selection with dataframe
            st.markdown("**Select rows by clicking on them:**")

            # Create selection dataframe
            selection_df = df_display[[
                'instruction_id', 'category', 'title', 'priority', 'active']].copy()

            selected_rows = st.dataframe(
                selection_df,
                use_container_width=True,
                on_select="rerun",
                selection_mode="multi-row"
            )

            if selected_rows and 'selection' in selected_rows and 'rows' in selected_rows['selection']:
                selected_indices = selected_rows['selection']['rows']
                st.session_state.selected_instructions = [
                    selection_df.iloc[i]['instruction_id'] for i in selected_indices
                ]

        # Show selected count
        st.info(
            f"📋 Selected {len(st.session_state.selected_instructions)} instructions")

        # Quick actions
        quick_col1, quick_col2, quick_col3 = st.columns(3)
        with quick_col1:
            if st.button("🔄 Select All Active", use_container_width=True):
                active_ids = df_display[df_display['active']
                                        == True]['instruction_id'].tolist()
                st.session_state.selected_instructions = active_ids
                st.rerun()

        with quick_col2:
            if st.button("⭐ Select High Priority", use_container_width=True):
                high_priority_ids = df_display[df_display['priority']
                                               >= 3]['instruction_id'].tolist()
                st.session_state.selected_instructions = high_priority_ids
                st.rerun()

        with quick_col3:
            if st.button("🗑️ Clear Selection", use_container_width=True):
                st.session_state.selected_instructions = []
                st.rerun()

    with col_template:
        st.subheader("📝 Template Configuration")

        # Template editor
        template_text = st.text_area(
            "Jinja2 Template",
            value=st.session_state.prompt_template,
            height=300,
            help="Use Jinja2 syntax. Available variables: instructions (list of selected instruction objects)"
        )

        st.session_state.prompt_template = template_text




        # Template preview
        st.subheader("👀 Template Preview")

        if st.session_state.selected_instructions:
            # Get selected data
            selected_data = get_selected_data()

            # Render template
            rendered_prompt = _render_template(
                st.session_state.prompt_template,
                {'instructions': selected_data}
            )

            # Show preview
            st.code(rendered_prompt, language="markdown")

            # Actions
            action_col1, action_col2 = st.columns(2)

            with action_col1:
                if st.button("📋 Use as Current Prompt", use_container_width=True):
                    st.session_state.current_prompt = rendered_prompt
                    st.success("✅ Template applied to current prompt!")

            with action_col2:
                if st.button("💾 Save Template Version", use_container_width=True):
                    description = f"Template with {len(st.session_state.selected_instructions)} instructions"
                    if save_prompt_version(rendered_prompt, description):
                        st.success("✅ Template version saved!")
                    else:
                        st.info("ℹ️ This template version already exists")

        else:
            st.info("Select instructions from the left panel to see template preview")

        # Template presets
        st.subheader("📋 Template Presets")

        selected_preset = st.selectbox(
            "Choose a preset template:", list(PRESET_TEMPLATES.keys()))

        if st.button("📥 Load Preset", use_container_width=True):
            st.session_state.prompt_template = PRESET_TEMPLATES[selected_preset]
            st.rerun()


def _render_template(template_str: str, data: Dict) -> str:
    """Render Jinja2 template with provided data"""
    try:
        template = Template(template_str)
        return template.render(**data)
    except Exception as e:
        return f"Template Error: {str(e)}"


PRESET_TEMPLATES = {
    "Basic List": """# System Instructions
{% for instruction in instructions %}
- {{ instruction.title }}: {{ instruction.content }}
{% endfor %}""",
    "Categorized": """# System Instructions
{% set categories = instructions | groupby('category') %}
{% for category, items in categories %}
## {{ category }}
{% for instruction in items %}
- **{{ instruction.title }}**: {{ instruction.content }}
{% endfor %}
{% endfor %}""",
    "Priority Based": """# System Instructions
{% for instruction in instructions | sort(attribute='priority', reverse=true) %}
{% if instruction.priority >= 3 %}⭐ {% endif %}**{{ instruction.title }}**
{{ instruction.content }}
{% endfor %}""",
    "Detailed Format": """# System Instructions
{% for instruction in instructions %}
## {{ instruction.category }}: {{ instruction.title }}
**Instruction ID:** {{ instruction.instruction_id }}
**Priority:** {{ instruction.priority }}/5
**Status:** {{ "Active" if instruction.active else "Inactive" }}
### Content:
{{ instruction.content }}
---
{% endfor %}"""
}
