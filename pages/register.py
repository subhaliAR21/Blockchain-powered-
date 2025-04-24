import streamlit as st
from db.firebase_app import register
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces, is_valid_email

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

form = st.form("login")
email = form.text_input("Enter your email", label_visibility="visible")
password = form.text_input("Enter your password", type="password", label_visibility="visible")
clicked_login = st.button("Already registered? Click here to login!")

if clicked_login:
    switch_page("login")
    
submit = form.form_submit_button("Register")
if submit:
    if not email or not password:
        st.error("Please enter both email and password.")
    elif not is_valid_email(email):
        st.error("Please enter a valid email address.")
    else:
        result = register(email, password)
        if result == "success":
            st.success("Registration successful!")
            if st.session_state.profile == "Institute":
                switch_page("institute")
            else:
                switch_page("verifier")
        elif result == "email_exists":
            st.error("This email is already registered. Please login or use a different email.")
        else:
            st.error("Registration unsuccessful!")
