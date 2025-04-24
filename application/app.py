import sys
import os
import streamlit as st
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'application')))
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

st.title("Certificate Validation System")
st.write("")
st.subheader("Select Your Role")

col1, col2 = st.columns(2)
institute_logo = Image.open("assets/institute_logo.png")
with col1:
    st.image(institute_logo, output_format="jpg", width=230)
    clicked_institute = st.button("Institute", help="Click to login as an Institute")

company_logo = Image.open("assets/company_logo.jpg")
with col2:
    st.image(company_logo, output_format="jpg", width=230)
    clicked_verifier = st.button("Verifier", help="Click to login as a Verifier")

if clicked_institute:
    st.session_state.profile = "Institute"
    switch_page('login')
elif clicked_verifier:
    st.session_state.profile = "Verifier"
    switch_page('login')
