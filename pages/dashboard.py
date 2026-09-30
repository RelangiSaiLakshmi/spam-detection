"""Dashboard page: welcome, statistics, shortcuts and recent checks."""
import pandas as pd
import streamlit as st

import database as db
from utils import AWARE, CHECK, MYREP, SAFETY, go


def render():
    user = st.session_state["user"]
    st.title(f"👋 Welcome, {user['name']}!")
    st.write("Stay safe while looking for internships. Check offers before you apply or pay.")

    try:
        stats = db.get_stats(user["id"])
        checks = db.get_checks(user["id"])
    except Exception:
        st.error("Could not load your data.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("🔍 Internships Checked", stats["checked"])
    c2.metric("🚨 Potential Spams Detected", stats["spams"])
    c3.metric("📋 Reports Submitted", stats["reports"])

    st.subheader("Quick Actions")
    a, b, c, d = st.columns(4)
    if a.button("🔍 Check Internship", type="primary", use_container_width=True):
        go(CHECK)
    if b.button("📋 My Reports", use_container_width=True):
        go(MYREP)
    if c.button("🛡️ Spam Awareness Tips", use_container_width=True):
        go(AWARE)
    if d.button("🔐 Safety Recommendations", use_container_width=True):
        go(SAFETY)

    st.subheader("Recent Checks")
    if checks:
        df = pd.DataFrame(checks).rename(columns={
            "company_name": "Company", "internship_title": "Title", "risk_score": "Score",
            "risk_level": "Level", "created_at": "Checked On"})
        left, right = st.columns([2, 1])
        left.dataframe(df.head(10), use_container_width=True, hide_index=True)
        counts = (df["Level"].value_counts()
                  .reindex(["Low Risk", "Medium Risk", "High Risk"], fill_value=0))
        right.caption("Your checks by risk level")
        right.bar_chart(counts)
    else:
        st.info("You have not checked any internship yet. Click 'Check Internship' to start.")

    with st.expander("💡 Tip of the day"):
        st.write("A real internship never asks you to pay money. If someone asks for a fee, stop and verify.")
