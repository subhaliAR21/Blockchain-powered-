from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import pdfplumber
import qrcode
import os
import tempfile

def generate_certificate(output_path, uid, candidate_name, course_name, org_name, institute_logo_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []

    if institute_logo_path:
        logo = RLImage(institute_logo_path, width=150, height=150)
        elements.append(logo)

    # Generate QR code for certificate verification
    certificate_id = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
    import hashlib
    certificate_hash = hashlib.sha256(certificate_id).hexdigest()
    qr = qrcode.make(certificate_hash)

    # Save QR code to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_qr_file:
        qr_path = tmp_qr_file.name
        qr.save(qr_path)

    # Add QR code image to PDF
    qr_image = RLImage(qr_path, width=100, height=100)
    elements.append(qr_image)

    institute_style = ParagraphStyle(
        "InstituteStyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica-Bold",
        fontSize=15,
        spaceAfter=40,
    )
    institute = Paragraph(org_name, institute_style)
    elements.extend([institute, Spacer(1, 12)])

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica-Bold",
        fontSize=25,
        spaceAfter=20,
    )
    title1 = Paragraph("Certificate of Completion", title_style)
    elements.extend([title1, Spacer(1, 6)])

    recipient_style = ParagraphStyle(
        "RecipientStyle",
        parent=getSampleStyleSheet()["BodyText"],
        fontSize=14,
        spaceAfter=6,
        leading=18,
        alignment=1
    )

    recipient_text = f"This is to certify that<br/><br/>\
                     <font color='red'> {candidate_name} </font><br/>\
                     with UID <br/> \
                    <font color='red'> {uid} </font> <br/><br/>\
                     has successfully completed the course:<br/>\
                     <font color='blue'> {course_name} </font>"

    recipient = Paragraph(recipient_text, recipient_style)
    elements.extend([recipient, Spacer(1, 12)])

    doc.build(elements)

    # Remove temporary QR code image file
    if os.path.exists(qr_path):
        os.remove(qr_path)

    print(f"Certificate generated and saved at: {output_path}")

from pyzbar.pyzbar import decode
from PIL import Image

def extract_certificate(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        lines = text.splitlines()

        org_name = lines[0]
        candidate_name = lines[3]
        uid = lines[5]
        course_name = lines[-1]

        return (uid, candidate_name, course_name, org_name)

def decode_qr_code(image_path):
    """
    Decode the QR code from the given image file and return the decoded data as string.
    """
    img = Image.open(image_path)
    decoded_objects = decode(img)
    if decoded_objects:
        return decoded_objects[0].data.decode('utf-8')
    else:
        return None
