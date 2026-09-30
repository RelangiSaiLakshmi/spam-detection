"""Rule-based internship spam-risk analysis.

analyze_internship(data) adds weighted points for each suspicious indicator
found (score is capped at 100) and returns the score, level and warnings.
This is only a RISK ASSESSMENT, never proof that an offer is a spam.
"""
import re

# ---------- keyword lists (easy to edit) ----------
FEE_WORDS = ["registration fee", "application fee", "training fee", "processing fee",
             "security deposit", "refundable deposit", "kit fee", "certificate fee",
             "admin fee", "registration charges", "pay a fee", "send money"]
BEFORE_SELECTION_WORDS = ["before selection", "before joining", "pay first", "pay before",
                          "advance payment", "deposit", "refundable"]
GUARANTEE_WORDS = ["guaranteed", "100% placement", "100% job", "assured job",
                   "assured placement", "job guarantee", "placement guarantee", "confirmed job"]
URGENT_WORDS = ["apply immediately", "apply now", "urgent", "urgently", "limited seats",
                "limited slots", "hurry", "today only", "immediate joining", "act fast",
                "offer expires", "few seats left", "last chance", "don't miss", "dont miss"]
SENSITIVE_WORDS = ["otp", "password", "aadhaar", "aadhar", "pan card", "bank account",
                   "account number", "cvv", "debit card", "credit card", "upi pin",
                   "atm pin", "passport copy"]
CHAT_WORDS = ["whatsapp", "telegram", "signal app", "dm us", "dm me"]
UNREALISTIC_WORDS = ["earn lakhs", "no interview", "without interview", "direct selection",
                     "easy money", "get rich", "earn daily", "daily payment", "instant offer",
                     "no test", "work 1 hour", "work 2 hours", "1 hour a day", "2 hours a day"]
LOW_EFFORT_WORDS = ["no experience", "no skills", "part time", "part-time", "few hours",
                    "1 hour", "2 hours", "simple task", "typing", "data entry",
                    "copy paste", "form filling", "like posts"]

PERSONAL_DOMAINS = {"gmail.com", "yahoo.com", "yahoo.in", "outlook.com", "hotmail.com",
                    "rediffmail.com", "protonmail.com", "icloud.com", "live.com",
                    "ymail.com", "aol.com"}
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "cutt.ly", "rb.gy", "is.gd"}
SUSPICIOUS_TLDS = (".xyz", ".top", ".click", ".buzz", ".tk", ".ml", ".ga", ".cf", ".gq", ".work", ".loan")
FREE_BUILDERS = ("blogspot.", "wixsite.", "weebly.", "000webhostapp", "github.io",
                 "netlify.app", "forms.gle", "docs.google.com/forms", "linktr.ee")

HIGH_STIPEND = 30000           # per month, very high for an internship
MEDIUM_STIPEND = 15000         # high if the work sounds easy


def _find(text, keywords):
    """Return the first keyword found as a whole word/phrase, else None."""
    for kw in keywords:
        if re.search(r"(?<!\w)" + re.escape(kw) + r"(?!\w)", text):
            return kw
    return None


def _num(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _host(url):
    if not url:
        return ""
    if "://" not in url:
        url = "http://" + url
    host = url.split("://", 1)[1].split("/")[0].split(":")[0].lower()
    return host[4:] if host.startswith("www.") else host


def get_risk_level(score):
    if score <= 30:
        return "Low Risk"
    if score <= 60:
        return "Medium Risk"
    return "High Risk"


RECOMMENDATIONS = {
    "High Risk": "Do not pay any money or share sensitive information until the company "
                 "is independently verified.",
    "Medium Risk": "Proceed with caution. Verify the company through its official website, "
                   "LinkedIn page and a phone call before sharing documents or paying anything.",
    "Low Risk": "No major warning signs were found, but always verify the company "
                "independently and never pay money to get an internship.",
}


def analyze_internship(data):
    """data keys: company_name, title, description, website, email, stipend,
    fee, phone, duration, mode, location. Returns score, level, warnings, details."""
    get = lambda k: str(data.get(k) or "").strip()
    company, title, desc = get("company_name"), get("title"), get("description")
    website, email, phone = get("website"), get("email"), get("phone")
    stipend, fee = _num(data.get("stipend")), _num(data.get("fee"))
    text = " ".join([company, title, desc]).lower()
    hits = []

    def add(warning, why, points):
        hits.append({"warning": warning, "explanation": why, "points": points})

    # 1. Fees
    if fee > 0:
        add("Application/registration fee requested",
            "Genuine companies do not charge students to give them an internship. "
            "Fees are the most common spam tactic.", 25)
    elif _find(text, FEE_WORDS):
        add("Fee or payment mentioned in the description",
            "The text talks about a fee or deposit. Real internships do not ask you to pay.", 25)

    # 2. Money before selection
    if _find(text, BEFORE_SELECTION_WORDS):
        add("Money requested before selection or joining",
            "Being asked to pay a 'refundable' deposit or pay first is a classic trick. "
            "The money is rarely returned.", 15)

    # 3. Stipend
    easy = _find(text, LOW_EFFORT_WORDS)
    if stipend >= HIGH_STIPEND or (stipend >= MEDIUM_STIPEND and easy):
        add("Unusually high stipend",
            f"A stipend of Rs {stipend:,.0f}/month is very high for an internship"
            + (f" that sounds like easy work ('{easy}')." if easy else "."), 15)

    # 4. Guaranteed job
    if _find(text, GUARANTEE_WORDS):
        add("Guaranteed job or placement",
            "No honest company can guarantee a job. Selection depends on your skills and performance.", 20)

    # 5. Urgent language
    if _find(text, URGENT_WORDS):
        add("Urgent or pressure language",
            "Spammers rush you so you do not have time to verify the offer.", 10)

    # 6. Sensitive information
    if _find(text, SENSITIVE_WORDS):
        add("Requests sensitive personal information",
            "Passwords, OTPs, bank or ID details should never be shared during applications.", 20)

    # 7. Chat apps
    if _find(text, CHAT_WORDS):
        add("Communication through WhatsApp/Telegram",
            "Spammers prefer chat apps because they are hard to trace. Real companies use official email.", 10)

    # 8. Unrealistic promises
    if _find(text, UNREALISTIC_WORDS):
        add("Unrealistic promises",
            "Promises like 'no interview' or 'easy money' are too good to be true.", 10)

    # 9. Website
    host = _host(website)
    if not website:
        add("Missing website",
            "Every real company has a website. Without one you cannot verify who they are.", 10)
    else:
        problems = []
        if website.lower().startswith("http://"):
            problems.append("does not use secure HTTPS")
        if "." not in host:
            problems.append("does not look like a valid web address")
        if host in SHORTENERS:
            problems.append("is a shortened link")
        if host.endswith(SUSPICIOUS_TLDS):
            problems.append("uses a domain ending common on throwaway sites")
        if any(b in website.lower() for b in FREE_BUILDERS):
            problems.append("is hosted on a free site/form builder")
        if problems:
            add("Suspicious website",
                "The website " + "; ".join(problems) + ". Check it carefully.", 10)

    # 10. Email
    email_domain = email.split("@")[-1].lower() if "@" in email else ""
    if not email:
        add("No contact email provided", "A legitimate recruiter always has a contact email.", 5)
    elif email_domain in PERSONAL_DOMAINS:
        add("Personal email address used",
            f"Emails from @{email_domain} are free for anyone. Real companies use their own domain "
            "(e.g. hr@company.com).", 10)
    elif host and not (email_domain == host or email_domain.endswith("." + host)
                       or host.endswith("." + email_domain)):
        add("Email domain does not match website",
            "The email and website belong to different domains, which can mean impersonation.", 5)

    # 11. Poor description
    if len(desc.split()) < 25 or desc.count("!") >= 3:
        add("Poor or suspicious description",
            "The description is very short, vague or overly excited. Real offers describe "
            "tasks, skills and selection steps.", 8)

    # 12. Unverified company
    weak = [not website, not phone, (not email) or email_domain in PERSONAL_DOMAINS]
    if sum(weak) >= 2:
        add("Company details cannot be verified",
            "Two or more of website, phone number and official email are missing or weak.", 8)

    score = min(100, sum(h["points"] for h in hits))
    level = get_risk_level(score)
    return {
        "risk_score": score,
        "risk_level": level,
        "warnings": [h["warning"] for h in hits],
        "details": hits,
        "recommendation": RECOMMENDATIONS[level],
    }
