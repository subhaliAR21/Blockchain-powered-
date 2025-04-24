import streamlit as st
from db.firebase_app import login
from dotenv import load_dotenv
import os
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces, is_valid_email

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

if "profile" not in st.session_state:
    st.session_state.profile = None

load_dotenv()

form = st.form("login")
email = form.text_input("Enter your email", label_visibility="visible")
password = form.text_input("Enter your password", type="password", label_visibility="visible")

if st.session_state.profile != "Institute":
    clicked_register = st.button("New user? Click here to register!")

    if clicked_register:
        switch_page("register")

submit = form.form_submit_button("Login")
if submit:
    if not email or not password:
        st.error("Please enter both email and password.")
    elif not is_valid_email(email):
        st.error("Please enter a valid email address.")
    else:
        if st.session_state.profile == "Institute":
            valid_email = os.getenv("institute_email")
            valid_pass = os.getenv("institute_password")
            if email == valid_email and password == valid_pass:
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
