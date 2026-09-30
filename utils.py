"""Shared constants, sample data, styling and the navigation helper."""
import streamlit as st

# Sidebar page names
DASH = "🏠 Dashboard"
CHECK = "🔍 Check Internship"
RESULT = "📊 Spam Result"
AWARE = "🛡️ Spam Awareness"
SAFETY = "🔐 Safety Recommendations"
REPORT = "🚨 Report Spam"
MYREP = "📋 My Reports"
LOGOUT = "🚪 Logout"
PAGES = [DASH, CHECK, RESULT, AWARE, SAFETY, REPORT, MYREP, LOGOUT]

SPAM_TYPES = ["Asked for registration/application fee", "Fake job/internship offer",
              "Guaranteed placement spam", "Asked for sensitive personal information",
              "Fake company / impersonation", "Fake payment or cheque spam", "Other"]

WORK_MODES = ["Remote", "On-site", "Hybrid"]

# Sample data for testing (used by the buttons on the Check Internship page)
SAMPLES = {
    "High-risk sample": {
        "company": "GlobalTech Career Solutions",
        "title": "Data Entry Intern - Work From Home",
        "desc": "Earn Rs 40000 per month with only 2 hours of work daily! 100% job guarantee "
                "after internship. Apply immediately, limited seats. Pay a one-time registration "
                "fee of Rs 2500 (refundable). Send your Aadhaar and bank account details on "
                "WhatsApp to confirm your seat.",
        "website": "http://globaltech-careers.xyz", "email": "globaltech.hr@gmail.com",
        "stipend": 40000, "fee": 2500, "phone": "9876543210",
        "duration": "3 months", "mode": "Remote", "location": "Anywhere in India",
    },
    "Medium-risk sample": {
        "company": "Sparkle Startup Hub", "title": "Digital Marketing Intern",
        "desc": "Join our fast growing startup. Urgent hiring, apply now. Contact us on WhatsApp.",
        "website": "", "email": "hr.sparkle@yahoo.com", "stipend": 8000, "fee": 0,
        "phone": "", "duration": "2 months", "mode": "Remote", "location": "India",
    },
    "Low-risk sample": {
        "company": "BrightPath Software Pvt Ltd", "title": "Python Backend Intern",
        "desc": "We are looking for a Python intern to assist our backend team with building "
                "REST APIs, writing unit tests and documenting features. The intern will be "
                "mentored by a senior engineer and will join weekly code reviews. Selection is "
                "through an online aptitude test followed by a technical interview.",
        "website": "https://www.brightpath-software.com", "email": "careers@brightpath-software.com",
        "stipend": 15000, "fee": 0, "phone": "", "duration": "6 months",
        "mode": "Hybrid", "location": "Hyderabad",
    },
}

CSS = """
<style>
[data-testid="stSidebarNav"], [data-testid="stSidebarNavItems"] {display: none;}
[data-testid="stSidebar"] {background-color: #EEF4FF;}
h1, h2, h3 {color: #1E4FA8;}
div[data-testid="stMetric"] {background: #F4F8FF; border: 1px solid #D5E3FB;
    border-radius: 12px; padding: 12px 16px;}
.stButton > button {border-radius: 8px;}
</style>
"""


def go(page):
    """Switch sidebar page. The change is applied at the top of the next run."""
    st.session_state["pending_nav"] = page
    st.rerun()
