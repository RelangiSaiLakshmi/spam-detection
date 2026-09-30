"""Check Internship page: input form + validation, then run the detector."""
import re

import streamlit as st

import database as db
from spam_detector import analyze_internship
from utils import RESULT, SAMPLES, WORK_MODES, go

BLANK = {"company": "", "title": "", "desc": "", "website": "", "email": "",
         "stipend": 0, "fee": 0, "phone": "", "duration": "", "mode": "Remote", "location": ""}
EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def _load(values):
    for key, val in values.items():
        st.session_state["ci_" + key] = val


def _validate(d):
    errors = []
    if not d["company_name"]:
        errors.append("Company name is required.")
    if not d["title"]:
        errors.append("Internship title is required.")
    if len(d["description"]) > 5000:
        errors.append("Description is too long (max 5000 characters).")
    if d["email"] and not EMAIL_RE.match(d["email"]):
        errors.append("Contact email is not a valid email address.")
    if d["phone"] and not (7 <= len(re.sub(r"[\s+\-()]", "", d["phone"])) <= 15
                           and re.sub(r"[\s+\-()]", "", d["phone"]).isdigit()):
        errors.append("Phone number should contain 7-15 digits.")
    if len(d["website"]) > 200:
        errors.append("Website URL is too long.")
    return errors


def render():
    for key, val in BLANK.items():
        st.session_state.setdefault("ci_" + key, val)

    st.title("🔍 Check Internship")
    st.write("Enter the details of the offer you received. The more you fill in, the better the analysis.")

    st.caption("Want to try it out? Load some sample data:")
    cols = st.columns(4)
    for col, (name, values) in zip(cols, SAMPLES.items()):
        col.button(name, on_click=_load, args=(values,), use_container_width=True)
    cols[3].button("Clear form", on_click=_load, args=(BLANK,), use_container_width=True)

    with st.form("check_form"):
        c1, c2 = st.columns(2)
        company = c1.text_input("Company / Organization Name *", key="ci_company")
        title = c2.text_input("Internship Title *", key="ci_title")
        desc = st.text_area("Description (paste the offer text here)", key="ci_desc", height=140)
        c3, c4 = st.columns(2)
        website = c3.text_input("Website URL", key="ci_website", placeholder="https://company.com")
        email = c4.text_input("Contact Email", key="ci_email")
        c5, c6, c7 = st.columns(3)
        stipend = c5.number_input("Stipend (Rs per month)", min_value=0, step=500, key="ci_stipend")
        fee = c6.number_input("Registration / Application Fee (Rs)", min_value=0, step=100, key="ci_fee")
        phone = c7.text_input("Contact Phone Number", key="ci_phone")
        c8, c9, c10 = st.columns(3)
        duration = c8.text_input("Internship Duration", key="ci_duration", placeholder="e.g. 3 months")
        mode = c9.selectbox("Work Mode", WORK_MODES, key="ci_mode")
        location = c10.text_input("Location", key="ci_location")
        submitted = st.form_submit_button("🔎 Analyze Internship", type="primary")

    if not submitted:
        return

    data = {"company_name": company.strip(), "title": title.strip(), "description": desc.strip(),
            "website": website.strip(), "email": email.strip(), "stipend": stipend, "fee": fee,
            "phone": phone.strip(), "duration": duration.strip(), "mode": mode,
            "location": location.strip()}

    errors = _validate(data)
    if errors:
        for e in errors:
            st.error(e)
        return

    result = analyze_internship(data)
    try:
        db.save_check(st.session_state["user"]["id"], data, result)
    except Exception:
        st.warning("The analysis worked, but it could not be saved to your history.")
    st.session_state["last"] = {"data": data, "result": result}
    go(RESULT)
