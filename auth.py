"""Sign-up / login logic (PBKDF2 password hashing from Python's standard library)."""
import hashlib
import hmac
import os
import re

import streamlit as st

import database as db
from utils import DASH, go

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def hash_password(password):
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return salt.hex() + "$" + digest.hex()


def verify_password(password, stored):
    try:
        salt_hex, digest_hex = stored.split("$")
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                     bytes.fromhex(salt_hex), 200_000)
        return hmac.compare_digest(digest.hex(), digest_hex)
    except (ValueError, AttributeError):
        return False


def register_user(name, email, password, confirm):
    """Returns (ok, message)."""
    name, email = name.strip(), email.strip().lower()
    if len(name) < 2 or len(name) > 60:
        return False, "Please enter your name (2-60 characters)."
    if not EMAIL_RE.match(email):
        return False, "Please enter a valid email address."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if password != confirm:
        return False, "Passwords do not match."
    try:
        user_id = db.create_user(name, email, hash_password(password))
    except Exception:
        return False, "Could not create the account. Please try again."
    if user_id is None:
        return False, "An account with this email already exists."
    return True, "Account created! You can now log in."


def login_user(email, password):
    """Returns (user_dict_or_None, message). The password hash is never returned."""
    email = email.strip().lower()
    if not email or not password:
        return None, "Please enter your email and password."
    try:
        row = db.get_user_by_email(email)
    except Exception:
        return None, "Database error. Please try again."
    if row is None or not verify_password(password, row["password_hash"]):
        return None, "Incorrect email or password."
    return {"id": row["id"], "name": row["name"], "email": row["email"]}, "OK"


def show_auth_page():
    st.title("🛡️ AI Internship Spam Detection System")
    st.caption("Check internship offers for warning signs before you apply or pay.")
    tab_login, tab_signup = st.tabs(["🔐 Login", "📝 Sign Up"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", type="primary")
        if submitted:
            user, msg = login_user(email, password)
            if user:
                st.session_state["user"] = user
                go(DASH)
            else:
                st.error(msg)

    with tab_signup:
        with st.form("signup_form", clear_on_submit=False):
            name = st.text_input("Full name")
            email = st.text_input("Email address")
            password = st.text_input("Password (min 8 characters)", type="password")
            confirm = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Create account", type="primary")
        if submitted:
            ok, msg = register_user(name, email, password, confirm)
            (st.success if ok else st.error)(msg)
