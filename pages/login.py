import streamlit as st
from db.firebase_app import login
from dotenv import load_dotenv
import os
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces, is_valid_email, render_header, render_footer

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

# Header
render_header("Login to BlockVerify")

if "profile" not in st.session_state:
    st.session_state.profile = None

load_dotenv()

with st.form("login", clear_on_submit=False):
    email = st.text_input("Enter your email", label_visibility="visible", placeholder="you@example.com")
    password = st.text_input("Enter your password", type="password", label_visibility="visible", placeholder="Your password")
    submit = st.form_submit_button("Login")

if st.session_state.profile != "Institute":
    if st.button("New user? Click here to register!"):
        switch_page("register")

if submit:
    if not email or not password:
        st.error("Please enter both email and password.")
    elif not is_valid_email(email):
        st.error("Please enter a valid email address.")
    else:
        if st.session_state.profile == "Institute":
            valid_emails_str = os.getenv("institute_email", "")
            valid_pass = os.getenv("institute_password")
            # Split emails by space or slash
            valid_emails = [e.strip() for e in valid_emails_str.replace('/', ' ').split()]
            if email in valid_emails and password == valid_pass:
                switch_page("institute")
            else:
                st.error("Invalid credentials!")
        else:
            result = login(email, password)
            if result == "success":
                st.success("Login successful!")
                switch_page("verifier")
            elif result == "invalid_password":
                st.error("Invalid password. Please try again.")
            elif result == "email_not_found":
                st.error("Email not found. Please register first.")
            else:
                st.error("Invalid credentials!")

# Footer
render_footer()
