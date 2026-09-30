"""Entry point: streamlit run app.py"""
import streamlit as st

import database as db
from auth import show_auth_page
from pages import (awareness, check_internship, dashboard, my_reports,
                   report_spam, safety, spam_result)
from utils import (AWARE, CHECK, CSS, DASH, LOGOUT, MYREP, PAGES, REPORT,
                   RESULT, SAFETY)

st.set_page_config(page_title="AI Internship Spam Detection System",
                   page_icon="🛡️", layout="wide")
db.init_db()
st.markdown(CSS, unsafe_allow_html=True)

# Not logged in -> show login / signup
if "user" not in st.session_state:
    show_auth_page()
    st.stop()

# Apply a navigation request made by go() in the previous run
if "pending_nav" in st.session_state:
    st.session_state["nav"] = st.session_state.pop("pending_nav")
st.session_state.setdefault("nav", DASH)

st.sidebar.title("🛡️ Spam Detector")
st.sidebar.caption(f"Signed in as {st.session_state['user']['name']}")
st.sidebar.radio("Navigation", PAGES, key="nav", label_visibility="collapsed")

ROUTES = {
    DASH: dashboard.render, CHECK: check_internship.render, RESULT: spam_result.render,
    AWARE: awareness.render, SAFETY: safety.render, REPORT: report_spam.render,
    MYREP: my_reports.render,
}

choice = st.session_state["nav"]
if choice == LOGOUT:
    st.session_state.clear()
    st.rerun()

try:
    ROUTES[choice]()
except Exception as exc:  # basic error handling: never show a raw crash to the user
    st.error("Something went wrong. Please try again.")
    st.caption(f"Details: {type(exc).__name__}")
