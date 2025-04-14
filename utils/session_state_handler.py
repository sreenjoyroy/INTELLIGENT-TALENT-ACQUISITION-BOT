import streamlit as st

def initialize_session():
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'hr_details' not in st.session_state:
        st.session_state.hr_details = {}
    if 'applicant_details' not in st.session_state:
        st.session_state.applicant_details = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def get_session_data():
    return {
        "user_type": st.session_state.get("user_type", None),
        "hr_details": st.session_state.get("hr_details", {}),
        "applicant_details": st.session_state.get("applicant_details", {}),
        "chat_history": st.session_state.get("chat_history", []),
    }

def update_chat_history(user_input, bot_response):
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    st.session_state.chat_history.append({
        "user": user_input,
        "bot": bot_response
    })
