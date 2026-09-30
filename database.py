"""SQLite helpers: table creation and simple query functions."""
import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "spam_detector.db"


def get_conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they do not exist yet."""
    with closing(get_conn()) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS internship_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                company_name TEXT,
                internship_title TEXT,
                description TEXT,
                website TEXT,
                email TEXT,
                stipend REAL,
                application_fee REAL,
                risk_score INTEGER,
                risk_level TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );

            CREATE TABLE IF NOT EXISTS spam_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                company_name TEXT,
                internship_title TEXT,
                website TEXT,
                spam_type TEXT,
                description TEXT,
                contact_info TEXT,
                incident_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            """
        )
        conn.commit()


def _execute(sql, params=()):
    with closing(get_conn()) as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid


def _query(sql, params=()):
    with closing(get_conn()) as conn:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]


# ---------- users ----------
def create_user(name, email, password_hash):
    """Returns the new user id, or None if the email already exists."""
    try:
        return _execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
    except sqlite3.IntegrityError:
        return None


def get_user_by_email(email):
    rows = _query("SELECT * FROM users WHERE email = ?", (email,))
    return rows[0] if rows else None


# ---------- internship checks ----------
def save_check(user_id, data, result):
    return _execute(
        """INSERT INTO internship_checks
           (user_id, company_name, internship_title, description, website, email,
            stipend, application_fee, risk_score, risk_level)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            user_id, data["company_name"], data["title"], data["description"],
            data["website"], data["email"], data["stipend"], data["fee"],
            result["risk_score"], result["risk_level"],
        ),
    )


def get_checks(user_id):
    return _query(
        """SELECT company_name, internship_title, risk_score, risk_level, created_at
           FROM internship_checks WHERE user_id = ? ORDER BY id DESC""",
        (user_id,),
    )


# ---------- reports ----------
def save_report(user_id, company, title, website, spam_type, description, contact, incident_date):
    return _execute(
        """INSERT INTO spam_reports
           (user_id, company_name, internship_title, website, spam_type,
            description, contact_info, incident_date)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (user_id, company, title, website, spam_type, description, contact, incident_date),
    )


def get_reports(user_id):
    return _query(
        """SELECT id, company_name, internship_title, website, spam_type,
                  description, incident_date, created_at
           FROM spam_reports WHERE user_id = ? ORDER BY id DESC""",
        (user_id,),
    )


# ---------- statistics ----------
def get_stats(user_id):
    checked = _query("SELECT COUNT(*) AS n FROM internship_checks WHERE user_id = ?", (user_id,))[0]["n"]
    spams = _query(
        "SELECT COUNT(*) AS n FROM internship_checks WHERE user_id = ? AND risk_level = 'High Risk'",
        (user_id,),
    )[0]["n"]
    reports = _query("SELECT COUNT(*) AS n FROM spam_reports WHERE user_id = ?", (user_id,))[0]["n"]
    return {"checked": checked, "spams": spams, "reports": reports}
