import streamlit as st
import json
from PyPDF2 import PdfReader, PdfWriter
import tempfile
import os

st.title("📄 PDF Auto-Filler Demo (Extended)")

pdf_file = st.file_uploader("Upload PDF form (with fields)", type=["pdf"])
json_file = st.file_uploader("Upload JSON data", type=["json"])

if pdf_file and json_file:
    data = json.load(json_file)

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_file.read())
        temp_pdf_path = temp_pdf.name

    reader = PdfReader(temp_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Map checkbox value to boolean (non-empty means True)
    field_values = {}
    for key, value in data.items():
        if key == "citizen":
            field_values[key] = "/Yes" if str(value).lower() in ["yes", "true", "1"] else "/Off"
        else:
            field_values[key] = value

    # Fill form fields
    writer.update_page_form_field_values(writer.pages[0], field_values)

    # Output filled PDF
    output_path = "filled_output.pdf"
    with open(output_path, "wb") as f:
        writer.write(f)

    with open(output_path, "rb") as f:
        st.download_button("⬇️ Download filled PDF", f, file_name="filled_output.pdf")

    os.remove(temp_pdf_path)
    os.remove(output_path)
