import streamlit as st
import os
import hashlib
from utils.cert_utils import extract_certificate, decode_qr_code
from utils.streamlit_utils import view_certificate, displayPDF, hide_icons, hide_sidebar, remove_whitespaces
from application.connection import contract


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

options = ("Verify Certificate using PDF", "View/Verify Certificate using Certificate ID", "Verify Certificate using QR Code")
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

elif selected == options[2]:
    uploaded_qr = st.file_uploader("Upload the QR code image")
    if uploaded_qr is not None:
        qr_bytes = uploaded_qr.getvalue()
        with open("qr_code.png", "wb") as qr_file:
            qr_file.write(qr_bytes)
        try:
            with st.spinner("Decoding QR code..."):
                certificate_id = decode_qr_code("qr_code.png")
            if certificate_id is None:
                st.error("Could not decode QR code. Please upload a valid QR code image.")
            else:
                with st.spinner("Verifying certificate on blockchain..."):
                    result = contract.functions.isVerified(certificate_id).call()
                if result:
                    st.success("Certificate validated successfully!")
                    view_certificate(certificate_id)
                else:
                    st.error("Invalid Certificate ID from QR code!")
        except Exception as e:
            st.error("Error processing QR code verification.")
        finally:
            import os
            if os.path.exists("qr_code.png"):
                os.remove("qr_code.png")
