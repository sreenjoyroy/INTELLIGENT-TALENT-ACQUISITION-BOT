import streamlit as st
from chroma_db import db_handler
from email_utils.send_email import send_email_to_hr, send_email_to_applicant
from streamlit_chat import message
from utils.chat_handler import process_user_input,chatbot_interface
from utils.pdf_parser import extract_text_from_pdf
from utils.helper import save_uploaded_file
from chroma_db.db_handler import get_all_open_positions
from agents.screening_agent import ScreeningAgent
from agents.engagement_agent import EngagementAgent
from agents.scheduling_agent import SchedulingAgent
import os
import base64

st.set_page_config(page_title="Intelligent Talent Acquisition Assistant", layout="centered")
st.title("🤖 Intelligent Talent Acquisition Assistant")

st.markdown("---")

# Initialize session state for chat
if 'past' not in st.session_state:
    st.session_state.past = []
if 'generated' not in st.session_state:
    st.session_state.generated = []

# Chat interface
tabs = st.tabs(["💬 Chatbot Interface", "📄 Open Positions", "📎 Upload Resume"])

# Chat Tab
with tabs[0]:
    st.subheader("AI Chatbot")

    user_input = st.chat_input("Say something...")
    if user_input:
        response = chatbot_interface(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state.generated:
        for i in range(len(st.session_state.generated) - 1, -1, -1):
            message(st.session_state.generated[i], key=str(i))
            message(st.session_state.past[i], is_user=True, key=f"{i}_user")

# Open Positions Tab
with tabs[1]:
    st.subheader("📌 Available Open Positions")
    open_positions = get_all_open_positions()

    if open_positions and open_positions['documents']:
        for meta, doc in zip(open_positions['metadatas'], open_positions['documents']):
            st.markdown(f"**Company:** {meta['company']}")
            st.markdown(f"**Recruiter:** {meta['name']}")
            st.markdown(f"**Email:** {meta['email']}")
            st.markdown(f"**Position:** {meta['position']}")
            st.markdown(f"**Recruiter ID:** {meta['recruiter_id']}")
            st.info(doc)
            st.markdown("---")
    else:
        st.warning("No open positions found.")

# Resume Upload Tab
with tabs[2]:
    st.subheader("📎 Upload Your Resume")
    resume_file = st.file_uploader("Upload Resume (.pdf)", type=["pdf"])
    if resume_file:
        # Save and extract resume content
        resume_path = save_uploaded_file(resume_file)
        resume_text = extract_text_from_pdf(resume_path)
        st.success("✅ Resume uploaded successfully!")

# Global variables to hold state
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'hr_details' not in st.session_state:
    st.session_state.hr_details = {}
if 'applicant_details' not in st.session_state:
    st.session_state.applicant_details = {}

# Step 1: Identify User Type
st.subheader("Step 1: Who are you?")
user_type = st.radio("Select your role:", ["HR", "Applicant"])
st.session_state.user_type = user_type

st.markdown("---")

# Step 2: HR Form
if user_type == "HR":
    st.subheader("Step 2: HR Details")
    with st.form("hr_form"):
        name = st.text_input("Your Name")
        recruiter_id = st.text_input("Recruiter ID")
        email = st.text_input("Your Email")
        company = st.text_input("Company Name")
        position = st.text_input("Open Position")
        submitted = st.form_submit_button("Submit HR Details")

        if submitted:
            hr_data = {
                "name": name,
                "recruiter_id": recruiter_id,
                "email": email,
                "company": company,
                "position": position
            }
            db_handler.save_hr_to_db(hr_data)
            st.session_state.hr_details = hr_data
            st.success("✅ HR details submitted successfully!")

# Step 3: Applicant Form
elif user_type == "Applicant":
    st.subheader("Step 2: Applicant Details")
    open_positions = db_handler.get_all_open_positions()
    available_positions = [item['position'] for item in open_positions['metadatas']]

    with st.form("applicant_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        institute = st.text_input("Your Institute")
        yoe = st.number_input("Years of Experience", min_value=0)
        selected_position = st.selectbox("Select a Position to Apply", available_positions)
        free_date = st.date_input("Select Your Free Date")
        free_time = st.time_input("Select Your Free Time", value=None)
        resume_file = st.file_uploader("Upload Resume (.pdf)", type=["pdf"])
        submit_app = st.form_submit_button("Submit Application")

        if submit_app:
            if resume_file is not None:
                resume_path = save_uploaded_file(resume_file)
                resume_text = extract_text_from_pdf(resume_path)

                app_data = {
                    "name": name,
                    "email": email,
                    "institute": institute,
                    "yoe": yoe,
                    "position": selected_position,
                    "free_date": free_date.strftime("%Y-%m-%d"),
                    "free_time": free_time.strftime("%H:%M:%S")
                }
                db_handler.save_applicant_to_db(app_data, resume_text)
                st.session_state.applicant_details = app_data
                st.success("✅ Application submitted successfully!")
            else:
                st.warning("⚠️ Please upload your resume before submitting.")

# Step 4: Screening + Engagement + Scheduling
if st.session_state.user_type == "Applicant" and st.session_state.applicant_details:
    st.subheader("Step 3: Screening in Progress")

    screening_agent = ScreeningAgent()
    screening_result = screening_agent.run()
    st.success(f"📄 Screening Result: {screening_result}")

    if "Eligible" in screening_result:
        st.subheader("Step 4: Sending Engagement & Scheduling Emails")

        engagement_agent = EngagementAgent()
        engagement_result = engagement_agent.run()
        st.info(f"🗣️ Engagement: {engagement_result}")

        scheduling_agent = SchedulingAgent()
        interview_info = scheduling_agent.run()

        hr_email_sent = send_email_to_hr(
            hr_email=st.session_state.hr_details['email'],
            applicant_data=st.session_state.applicant_details,
            interview_info=interview_info
        )

        if hr_email_sent:
            applicant_email_sent = send_email_to_applicant(
                applicant_email=st.session_state.applicant_details['email'],
                hr_data=st.session_state.hr_details,
                interview_info=interview_info
            )
            if applicant_email_sent:
                st.success("📬 Emails sent successfully to HR and Applicant!")
            else:
                st.warning("⚠️ Failed to send email to applicant.")
        else:
            st.warning("⚠️ Failed to send email to HR. Please check HR email configuration.")