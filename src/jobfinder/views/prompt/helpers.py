
import streamlit as st
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
from jinja2 import Template, Environment, BaseLoader


def save_prompt_version(prompt: str, description: str = ""):
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
