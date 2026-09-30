"""Spam Result page: shows the latest analysis."""
import streamlit as st

from utils import CHECK, REPORT, SAFETY, go


def render():
    st.title("📊 Spam Result")
    last = st.session_state.get("last")
    if not last:
        st.info("No analysis yet. Check an internship first.")
        if st.button("Go to Check Internship", type="primary"):
            go(CHECK)
        return

    data, res = last["data"], last["result"]
    score, level = res["risk_score"], res["risk_level"]
    st.subheader(f"{data['company_name']} — {data['title']}")

    if level == "High Risk":
        st.error(f"🚨 Risk Level: {level.upper()}")
    elif level == "Medium Risk":
        st.warning(f"⚠️ Risk Level: {level.upper()}")
    else:
        st.success(f"✅ Risk Level: {level.upper()}")

    m1, m2, m3 = st.columns(3)
    m1.metric("Risk Score", f"{score}/100")
    m2.metric("Risk Level", level)
    m3.metric("Warning Signs", len(res["details"]))
    st.progress(score / 100)

    st.info("ℹ️ This is only a risk assessment based on simple rules. It is NOT a guaranteed "
            "determination that this internship is (or is not) a spam.")

    st.subheader("Warning Signs")
    if res["details"]:
        for item in res["details"]:
            with st.expander(f"✓ {item['warning']}  (+{item['points']} points)", expanded=True):
                st.write(item["explanation"])
    else:
        st.success("No suspicious indicators were found in the information you entered.")

    st.subheader("Recommendation")
    box = st.error if level == "High Risk" else st.warning if level == "Medium Risk" else st.success
    box(res["recommendation"])

    b1, b2, b3 = st.columns(3)
    if b1.button("🚨 Report This Internship", use_container_width=True):
        st.session_state["report_prefill"] = {"company": data["company_name"],
                                              "title": data["title"], "website": data["website"]}
        go(REPORT)
    if b2.button("🔍 Check Another Internship", use_container_width=True):
        go(CHECK)
    if b3.button("🔐 Safety Recommendations", use_container_width=True):
        go(SAFETY)
