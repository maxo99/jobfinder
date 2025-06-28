import streamlit as st
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
from jinja2 import Template, Environment, BaseLoader

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


def save_prompt_version(prompt: str, description: str = ""):
    """Save a version of the prompt to history"""
    version = {
        'id': hashlib.md5(prompt.encode()).hexdigest()[:8],
        'content': prompt,
        'description': description,
        'timestamp': datetime.now().isoformat(),
        'word_count': len(prompt.split()),
        'char_count': len(prompt)
    }

    # Check if this exact prompt already exists
    if not any(v['content'] == prompt for v in st.session_state.prompt_history):
        st.session_state.prompt_history.insert(0, version)
        # Keep only last 10 versions
        st.session_state.prompt_history = st.session_state.prompt_history[:10]
        return True
    return False


def load_prompt_from_history(version_id: str):
    """Load a prompt from history"""
    for version in st.session_state.prompt_history:
        if version['id'] == version_id:
            st.session_state.current_prompt = version['content']
            st.rerun()


def render_template(template_str: str, data: Dict) -> str:
    """Render Jinja2 template with provided data"""
    try:
        template = Template(template_str)
        return template.render(**data)
    except Exception as e:
        return f"Template Error: {str(e)}"



def validate_prompt(prompt: str) -> Dict[str, any]:
    validation = {
        'is_valid': True,
        'warnings': [],
        'stats': {
            'word_count': len(prompt.split()),
            'char_count': len(prompt),
            'line_count': len(prompt.split('\n')),
            'paragraph_count': len([p for p in prompt.split('\n\n') if p.strip()])
        }
    }

    if len(prompt) < 50:
        validation['warnings'].append("Prompt seems very short")
    if len(prompt) > 10000:
        validation['warnings'].append(
            "Prompt is very long - consider breaking it down")
    if not prompt.strip():
        validation['is_valid'] = False
        validation['warnings'].append("Prompt cannot be empty")

    return validation



def get_selected_data() -> List[Dict]:
    """Get selected instruction data as list of dictionaries"""
    if not st.session_state.selected_instructions:
        return []

    selected_df = st.session_state.template_data[
        st.session_state.template_data['instruction_id'].isin(
            st.session_state.selected_instructions)
    ]
    return selected_df.to_dict('records')


def _template_builder(save_prompt_version, render_template, get_selected_data):
    st.markdown(
        "Select instructions from the data table and generate system prompts using Jinja2 templates")

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

        # Template help
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

        # Template preview
        st.subheader("👀 Template Preview")

        if st.session_state.selected_instructions:
            # Get selected data
            selected_data = get_selected_data()

            # Render template
            rendered_prompt = render_template(
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

        preset_templates = {
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

        selected_preset = st.selectbox(
            "Choose a preset template:", list(preset_templates.keys()))

        if st.button("📥 Load Preset", use_container_width=True):
            st.session_state.prompt_template = preset_templates[selected_preset]
            st.rerun()


# Main UI
st.title("🤖 System Prompt Manager")
st.markdown(
    "Manage and update system prompts with version control and validation")


# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["📝 Edit Prompt", "📊 Analytics", "📚 History", "🔧 Template Builder"])

with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Current System Prompt")

        # Text area for prompt editing
        prompt_text = st.text_area(
            "System Prompt Content",
            value=st.session_state.current_prompt,
            height=400,
            help="Enter or modify your system prompt here",
            key="prompt_editor"
        )

        # Update current prompt
        st.session_state.current_prompt = prompt_text

        # Action buttons
        col_save, col_load, col_clear = st.columns(3)

        with col_save:
            description = st.text_input("Version Description (optional)",
                                        placeholder="e.g., Added new instructions for...")
            if st.button("💾 Save Version", use_container_width=True):
                if save_prompt_version(prompt_text, description):
                    st.success("✅ Version saved successfully!")
                else:
                    st.info("ℹ️ This prompt version already exists")

        with col_load:
            st.markdown("**Load from file:**")
            uploaded_file = st.file_uploader(
                "Choose a text file", type=['txt', 'md'])
            if uploaded_file is not None:
                content = uploaded_file.read().decode('utf-8')
                st.session_state.current_prompt = content
                st.rerun()

        with col_clear:
            st.markdown("**Actions:**")
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.current_prompt = ""
                st.rerun()

    with col2:
        st.subheader("Validation & Stats")

        # Validate current prompt
        validation = validate_prompt(prompt_text)

        # Display validation status
        if validation['is_valid']:
            st.success("✅ Prompt is valid")
        else:
            st.error("❌ Prompt has issues")

        # Display warnings
        if validation['warnings']:
            st.warning("⚠️ Warnings:")
            for warning in validation['warnings']:
                st.write(f"• {warning}")

        # Display stats
        st.subheader("📊 Statistics")
        stats = validation['stats']

        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Words", stats['word_count'])
            st.metric("Lines", stats['line_count'])

        with col_stat2:
            st.metric("Characters", stats['char_count'])
            st.metric("Paragraphs", stats['paragraph_count'])

        # Export options
        st.subheader("📤 Export")
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            st.code(prompt_text, language="text")
            st.info("Copy the text above to your clipboard")

        if st.button("💾 Download as TXT", use_container_width=True):
            st.download_button(
                label="Download",
                data=prompt_text,
                file_name=f"system_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

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
    st.subheader("🔧 Template Builder")
    _template_builder(save_prompt_version, render_template, get_selected_data)
