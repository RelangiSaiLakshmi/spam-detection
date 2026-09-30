"""My Reports page: shows only the logged-in user's reports."""
import pandas as pd
import streamlit as st

import database as db


def render():
    st.title("📋 My Reports")
    try:
        rows = db.get_reports(st.session_state["user"]["id"])
    except Exception:
        st.error("Could not load your reports.")
        return
    if not rows:
        st.info("You have not submitted any reports yet.")
        return
    df = pd.DataFrame(rows).rename(columns={
        "id": "ID", "company_name": "Company", "internship_title": "Title", "website": "Website",
        "spam_type": "Spam Type", "description": "Description",
        "incident_date": "Incident Date", "created_at": "Submitted On"})
    st.metric("Reports submitted", len(df))
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download as CSV", df.to_csv(index=False), "my_reports.csv", "text/csv")
