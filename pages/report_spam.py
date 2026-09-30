"""Report Spam page."""
from datetime import date

import streamlit as st

import database as db
from utils import SPAM_TYPES


def render():
    st.title("🚨 Report Spam")
    st.write("Help other students by reporting suspicious internships.")
    pre = st.session_state.get("report_prefill", {})

    with st.form("report_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        company = c1.text_input("Company Name *", value=pre.get("company", ""))
        title = c2.text_input("Internship Title *", value=pre.get("title", ""))
        website = st.text_input("Website", value=pre.get("website", ""))
        spam_type = st.selectbox("Spam Type", SPAM_TYPES)
        description = st.text_area("Description of suspicious activity *", height=140)
        c3, c4 = st.columns(2)
        contact = c3.text_input("Contact information (optional)")
        when = c4.date_input("Date", value=date.today(), max_value=date.today())
        submitted = st.form_submit_button("Submit Report", type="primary")

    if not submitted:
        return
    if not company.strip() or not title.strip():
        st.error("Company name and internship title are required.")
        return
    if len(description.strip()) < 10:
        st.error("Please describe what happened (at least 10 characters).")
        return
    if len(description) > 3000:
        st.error("Description is too long (max 3000 characters).")
        return
    try:
        db.save_report(st.session_state["user"]["id"], company.strip(), title.strip(),
                       website.strip(), spam_type, description.strip(), contact.strip(), str(when))
    except Exception:
        st.error("Could not save your report. Please try again.")
        return
    st.session_state.pop("report_prefill", None)
    st.success("Thank you. Your report has been submitted successfully.")
