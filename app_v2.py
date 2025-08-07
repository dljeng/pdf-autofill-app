import streamlit as st
import json
import yaml
from PyPDF2 import PdfReader, PdfWriter
import tempfile
import os
from datetime import date

st.title("📄 PDF Auto-Filler with YAML and Date Picker")

# Upload section
pdf_file = st.file_uploader("Upload PDF form (with fields)", type=["pdf"])
data_file = st.file_uploader("Upload JSON or YAML data", type=["json", "yml", "yaml"])

# Optional manual override for DOB
dob_input = st.date_input("Date of Birth override (optional)", format="YYYY-MM-DD")

if pdf_file and data_file:
    # Determine file format
    if data_file.name.endswith((".yaml", ".yml")):
        data = yaml.safe_load(data_file)
    else:
        data = json.load(data_file)

    # If user selected a manual DOB, override
    if dob_input:
        data["dob"] = dob_input.strftime("%Y-%m-%d")

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_file.read())
        temp_pdf_path = temp_pdf.name

    reader = PdfReader(temp_pdf_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    # Convert values (checkbox needs special value)
    field_values = {}
    for key, value in data.items():
        if key == "citizen":
            field_values[key] = "/Yes" if str(value).lower() in ["yes", "true", "1"] else "/Off"
        else:
            field_values[key] = str(value)

    writer.update_page_form_field_values(writer.pages[0], field_values)

    # Output filled PDF
    output_path = "filled_output.pdf"
    with open(output_path, "wb") as f:
        writer.write(f)

    with open(output_path, "rb") as f:
        st.download_button("⬇️ Download filled PDF", f, file_name="filled_output.pdf")

    os.remove(temp_pdf_path)
    os.remove(output_path)
