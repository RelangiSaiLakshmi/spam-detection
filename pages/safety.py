"""Safety Recommendations page."""
import streamlit as st

SECTIONS = {
    "🟦 Before applying": ["Research the company.", "Check the official website.",
                           "Verify the recruiter.", "Search for company reviews and online presence."],
    "🟨 During communication": ["Use official company email.", "Do not share OTPs or passwords.",
                                "Do not install unknown software.", "Avoid suspicious links."],
    "🟩 Before accepting": ["Read the internship offer carefully.", "Check stipend/payment conditions.",
                            "Confirm company details.", "Never pay unexpected fees."],
    "🟥 If a spam is suspected": ["Stop communication.", "Do not send money.",
                                  "Save screenshots and messages.",
                                  "Report the suspicious internship (use the Report Spam page)."],
}


def render():
    st.title("🔐 Safety Recommendations")
    cols = st.columns(2)
    for i, (title, items) in enumerate(SECTIONS.items()):
        with cols[i % 2]:
            with st.container(border=True):
                st.subheader(title)
                for item in items:
                    st.markdown(f"✅ {item}")
    st.info("If you already lost money, contact your bank immediately and report it to the "
            "national cyber crime portal (cybercrime.gov.in in India) or your local police.")
