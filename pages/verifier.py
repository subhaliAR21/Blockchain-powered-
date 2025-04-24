import streamlit as st
import os
import hashlib
from utils.cert_utils import extract_certificate
from utils.streamlit_utils import view_certificate, displayPDF, hide_icons, hide_sidebar, remove_whitespaces
from application.connection import contract

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

options = ("Verify Certificate using PDF", "View/Verify Certificate using Certificate ID")
selected = st.selectbox("Select an option", options, label_visibility="hidden")

if selected == options[0]:
    uploaded_file = st.file_uploader("Upload the PDF version of the certificate")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        with open("certificate.pdf", "wb") as file:
            file.write(bytes_data)
        try:
            with st.spinner("Extracting certificate data..."):
                (uid, candidate_name, course_name, org_name) = extract_certificate("certificate.pdf")
            displayPDF("certificate.pdf")
            os.remove("certificate.pdf")

            data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
            certificate_id = hashlib.sha256(data_to_hash).hexdigest()

            with st.spinner("Verifying certificate on blockchain..."):
                result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Certificate validated successfully!")
            else:
                st.error("Invalid Certificate! Certificate might be tampered")
        except Exception as e:
            st.error("Invalid Certificate! Certificate might be tampered")

elif selected == options[1]:
    form = st.form("Validate-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Validate")
    if submit:
        try:
            view_certificate(certificate_id)
            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Certificate validated successfully!")
            else:
                st.error("Invalid Certificate ID!")
        except Exception as e:
            st.error("Invalid Certificate ID!")
