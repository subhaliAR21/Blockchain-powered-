import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
from utils.cert_utils import generate_certificate
from utils.streamlit_utils import view_certificate
from application.connection import contract, w3
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

load_dotenv()

api_key = os.getenv("PINATA_API_KEY")
api_secret = os.getenv("PINATA_API_SECRET")

def upload_to_pinata(file_path, api_key, api_secret):
    pinata_api_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": api_key,
        "pinata_secret_api_key": api_secret,
    }
    with open(file_path, "rb") as file:
        files = {"file": (file.name, file)}
        response = requests.post(pinata_api_url, headers=headers, files=files)
        result = json.loads(response.text)
        if "IpfsHash" in result:
            ipfs_hash = result["IpfsHash"]
            print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
            return None

options = ("Generate Certificate", "View Certificates")
selected = st.selectbox("Select an option", options, label_visibility="hidden")

if selected == options[0]:
    form = st.form("Generate-Certificate")
    uid = form.text_input(label="UID")
    candidate_name = form.text_input(label="Name")
    course_name = form.text_input(label="Course Name")
    org_name = form.text_input(label="Org Name")

    submit = form.form_submit_button("Submit")
    if submit:
        pdf_file_path = "certificate.pdf"
        institute_logo_path = "assets/logo.jpg"
        with st.spinner("Generating certificate..."):
            from reportlab.platypus import Image as RLImage
            # Use RLImage explicitly to avoid conflict with PIL.Image
            logo = RLImage(institute_logo_path, width=150, height=150)
            generate_certificate(pdf_file_path, uid, candidate_name, course_name, org_name, institute_logo_path)

        with st.spinner("Uploading certificate to IPFS..."):
            ipfs_hash = upload_to_pinata(pdf_file_path, api_key, api_secret)
        os.remove(pdf_file_path)

        if ipfs_hash is None:
            st.error("Failed to upload certificate to IPFS.")
        else:
            data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
            certificate_id = hashlib.sha256(data_to_hash).hexdigest()

            # Generate QR code image for download
            import qrcode
            import io
            qr_data = certificate_id
            qr_img = qrcode.make(qr_data)
            buf = io.BytesIO()
            qr_img.save(buf, format="PNG")
            buf.seek(0)

            st.download_button(
                label="Download Certificate QR Code",
                data=buf,
                file_name=f"certificate_{certificate_id}_qr.png",
                mime="image/png"
            )

        try:
            with st.spinner("Recording certificate on blockchain..."):
                contract.functions.generateCertificate(certificate_id, uid, candidate_name, course_name, org_name, ipfs_hash).transact({'from': w3.eth.accounts[0]})
            st.success(f"Certificate successfully generated with Certificate ID: {certificate_id}")
        except Exception as e:
            st.error(f"Failed to record certificate on blockchain: {str(e)}")

else:
    form = st.form("View-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Submit")
    if submit:
        try:
            view_certificate(certificate_id)
        except Exception as e:
            st.error("Invalid Certificate ID!")
