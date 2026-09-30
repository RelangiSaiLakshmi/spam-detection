"""Spam Awareness page."""
import streamlit as st

TIPS = [
    ("💸 Never pay money to get an internship",
     "Real companies pay interns, not the other way round. Registration, training, kit or "
     "'security deposit' fees are red flags."),
    ("🌐 Verify the company website and contact details",
     "Check that the website looks professional, uses HTTPS, and that the email domain matches it."),
    ("🎯 Be careful with guaranteed job offers",
     "Nobody can guarantee a job or placement. Selection always depends on your skills."),
    ("🔎 Check the company's online presence",
     "Look for a LinkedIn page, news, reviews and real employees. A brand-new company with no "
     "footprint deserves extra checking."),
    ("🔒 Protect passwords, OTPs, bank details and IDs",
     "Never share these during an application. Share only what is needed, and only after verifying."),
    ("💰 Be suspicious of extremely high stipends",
     "Very high pay for very little work is a common bait to make you ignore other warning signs."),
    ("⏰ Do not trust pressure tactics",
     "'Apply immediately' and 'only 3 seats left' are used to stop you from thinking."),
    ("📧 Verify offers through official channels",
     "Contact the company using the phone number or email listed on its official website, "
     "not the one in the message you received."),
]


def render():
    st.title("🛡️ Spam Awareness")
    st.write("Simple tips to recognise fake internship and job offers.")
    cols = st.columns(2)
    for i, (title, text) in enumerate(TIPS):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.write(text)

    with st.expander("Common spam patterns"):
        st.markdown(
            "- A 'recruiter' contacts you first on WhatsApp/Telegram.\n"
            "- You are 'selected' without any interview.\n"
            "- You are sent a cheque or asked to pay a fee 'to be refunded later'.\n"
            "- The offer letter has spelling mistakes or a personal email address.")
