
import streamlit as st

from jobfinder.views.prompt.helpers import save_prompt_version, validate_prompt


def render():
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

        # # Export options
        # st.subheader("📤 Export")
        # if st.button("📋 Copy to Clipboard", use_container_width=True):
        #     st.code(prompt_text, language="text")
        #     st.info("Copy the text above to your clipboard")

        # if st.button("💾 Download as TXT", use_container_width=True):
        #     st.download_button(
        #         label="Download",
        #         data=prompt_text,
        #         file_name=f"system_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        #         mime="text/plain"
        #     )
