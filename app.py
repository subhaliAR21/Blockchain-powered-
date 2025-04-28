import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
from PIL import Image

from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces, render_header, render_footer
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

# Header
render_header("BlockVerify – Blockchain-powered Certificate Verification System")

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

# Footer
render_footer()
