
import streamlit as st
from datetime import datetime
from typing import Dict, List
import hashlib

VERSIONS_LIMIT = 10

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
        st.session_state.prompt_history = st.session_state.prompt_history[:VERSIONS_LIMIT]
        return True
    return False


def get_prompt_stats(prompt: str) -> Dict[str, int]:
    return {
        'word_count': len(prompt.split()),
        'char_count': len(prompt),
        'line_count': len(prompt.split('\n')),
        'paragraph_count': len([p for p in prompt.split('\n\n') if p.strip()])
    }


def validate_prompt(prompt: str) -> Dict[str, any]:
    validation = {
        'is_valid': True,
        'warnings': [],
        'stats': get_prompt_stats(prompt)
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
