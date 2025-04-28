import streamlit as st
import base64
import requests
import os
import re
from application.connection import contract

def displayPDF(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def view_certificate(certificate_id):
    result = contract.functions.getCertificate(certificate_id).call()
    ipfs_hash = result[4]
    pinata_gateway_base_url = 'https://gateway.pinata.cloud/ipfs'
    content_url = f"{pinata_gateway_base_url}/{ipfs_hash}"
    response = requests.get(content_url)
    with open("temp.pdf", 'wb') as pdf_file:
        pdf_file.write(response.content)
    displayPDF("temp.pdf")
    os.remove("temp.pdf")

def hide_icons():
    hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>"""
    st.markdown(hide_st_style, unsafe_allow_html=True)

def hide_sidebar():
    no_sidebar_style = """
       <style>
          div[data-testid="stSidebarNav"] {visibility: hidden;}
       </style>"""
    st.markdown(no_sidebar_style, unsafe_allow_html=True)

def remove_whitespaces():
    st.markdown("""
        <style>
            /* Background image with overlay */
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-image: url('/assets/background.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                position: relative;
                min-height: 100vh;
                margin: 0;
                padding: 0;
                color: #f0f0f0;
            }
            /* Overlay to darken background for readability */
            body::before {
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: -1;
            }
            /* Padding and margin adjustments */
            .css-18e3th9 {
                padding-top: 2rem !important;
                padding-bottom: 5rem !important;
                padding-left: 3rem !important;
                padding-right: 3rem !important;
            }
            .css-1d391kg {
                padding-top: 3.5rem !important;
                padding-right: 1rem !important;
                padding-bottom: 3.5rem !important;
                padding-left: 1rem !important;
            }
            /* Button styling */
            div.stButton > button {
                background-color: #0078d4;
                color: white;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 16px;
                font-weight: 600;
                transition: background-color 0.3s ease;
                border: none;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            div.stButton > button:hover {
                background-color: #005a9e;
                cursor: pointer;
            }
            /* Input box styling */
            div.stTextInput > div > input {
                border-radius: 6px;
                border: 1px solid #ccc;
                padding: 10px;
                font-size: 16px;
                transition: border-color 0.3s ease;
            }
            div.stTextInput > div > input:focus {
                border-color: #0078d4;
                outline: none;
            }
            /* Header styles */
            .app-header {
                font-size: 2.5rem;
                font-weight: 700;
                color: #0078d4;
                margin-bottom: 1rem;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            /* Footer styles */
            .app-footer {
                font-size: 0.9rem;
                color: #888888;
                text-align: center;
                margin-top: 3rem;
                padding-top: 1rem;
                border-top: 1px solid #e1e1e1;
            }
        </style>
    """, unsafe_allow_html=True)

def is_valid_email(email: str) -> bool:
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None

def render_header(title: str):
    st.markdown(f'<h1 class="app-header">{title}</h1>', unsafe_allow_html=True)

def render_footer():
    st.markdown('<div class="app-footer">© 2025 BlockVerify. All rights reserved.</div>', unsafe_allow_html=True)