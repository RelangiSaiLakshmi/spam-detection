# 🛡️ AI Internship Spam Detection System

## Objective
Help students spot potentially fake internship/job offers. The user enters the details of an
offer; an intelligent **rule-based** analyzer gives a 0–100 spam-risk score, lists the warning
signs with explanations, and suggests what to do next.

> ⚠️ The result is only a **risk assessment**, not proof that an offer is or is not a spam.

## Features
- Sign up / login (passwords hashed with PBKDF2-SHA256 + random salt), logout
- Dashboard with statistics (internships checked, potential spams, reports submitted)
- Check Internship form with input validation and built-in sample data
- Result page: risk level, score, progress bar, warning signs with explanations, recommendation
- Report Spam form (stored in SQLite) and My Reports page (with CSV download)
- Spam Awareness and Safety Recommendations pages

## Technologies
Python 3.9+, Streamlit, SQLite (`sqlite3`), Pandas. No ML models, no paid APIs.

## Project Structure
```
ai_internship_spam_detector/
├── app.py              # entry point, sidebar navigation
├── database.py         # SQLite tables + queries
├── auth.py             # hashing, signup, login, login screen
├── spam_detector.py    # analyze_internship() rules
├── utils.py            # constants, sample data, CSS, go() navigation helper
├── requirements.txt
├── .streamlit/config.toml   # blue/white theme
├── pages/              # one file per page, each with render()
│   ├── dashboard.py  check_internship.py  spam_result.py  awareness.py
│   └── safety.py  report_spam.py  my_reports.py
└── data/spam_detector.db   # created automatically
```

## Installation
```
pip install -r requirements.txt
```

## How to Run
```
streamlit run app.py
```
Open the link shown in the terminal (usually http://localhost:8501), sign up, then log in.

## How the Detection Algorithm Works
`analyze_internship(data)` starts at 0 and adds points for every warning sign found:

| Warning sign | Points |
|---|---|
| Application/registration fee (field > 0 or mentioned) | +25 |
| Guaranteed job/placement | +20 |
| Requests sensitive info (OTP, password, Aadhaar, bank details) | +20 |
| Money before selection/joining (deposit, "refundable") | +15 |
| Very high stipend (≥ Rs 30,000/month, or ≥ Rs 15,000 for easy work) | +15 |
| Urgent language ("apply immediately", "limited seats") | +10 |
| Personal email (gmail, yahoo …) | +10 |
| Missing website / suspicious website (no HTTPS, shortener, odd domain) | +10 |
| WhatsApp/Telegram communication | +10 |
| Unrealistic promises ("no interview", "easy money") | +10 |
| Poor/very short description | +8 |
| Company details cannot be verified | +8 |
| No email, or email domain ≠ website domain | +5 |

The total is capped at 100. **0–30 = Low Risk, 31–60 = Medium Risk, 61–100 = High Risk.**
Keyword lists and weights are at the top of `spam_detector.py` and are easy to edit.

## Sample Test Data
Use the buttons on the *Check Internship* page, or type these:

| Sample | Company / Title | Website | Email | Stipend | Fee | Expected |
|---|---|---|---|---|---|---|
| High | GlobalTech Career Solutions / Data Entry Intern | http://globaltech-careers.xyz | globaltech.hr@gmail.com | 40000 | 2500 | High (100) |
| Medium | Sparkle Startup Hub / Digital Marketing Intern | *(none)* | hr.sparkle@yahoo.com | 8000 | 0 | Medium (56) |
| Low | BrightPath Software Pvt Ltd / Python Backend Intern | https://www.brightpath-software.com | careers@brightpath-software.com | 15000 | 0 | Low (0) |

## Notes
- Streamlit automatically detects a folder named `pages/`; the app hides that default menu with
  CSS and uses its own sidebar instead.
- The database file is created in `data/` on first run. Delete it to reset all data.
