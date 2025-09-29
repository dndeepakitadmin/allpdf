import streamlit as st
from pdf2docx import Converter
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from fpdf import FPDF
from PIL import Image
import pandas as pd
import os
import tempfile

st.set_page_config(page_title="All-in-One PDF Tool", layout="wide")
st.title("📄 All-in-One PDF Tool")

# Create temporary folder
tmp_dir = tempfile.mkdtemp()

# -----------------------
# PDF → DOCX
# -----------------------
st.header("PDF → DOCX")
pdf_file = st.file_uploader("Upload PDF for conversion", type="pdf", key="pdf2docx")
if pdf_file:
    output_path = os.path.join(tmp_dir, "converted.docx")
    with open(os.path.join(tmp_dir, pdf_file.name), "wb") as f:
        f.write(pdf_file.getbuffer())
    converter = Converter(os.path.join(tmp_dir, pdf_file.name))
    converter.convert(output_path, start=0, end=None)
    converter.close()
    st.success("PDF converted to DOCX successfully!")
    st.download_button("Download DOCX", output_path, "converted.docx")

# -----------------------
# PDF → Images
# -----------------------
st.header("PDF → Images")
pdf_img_file = st.file_uploader("Upload PDF to convert to images", type="pdf", key="pdf2img")
if pdf_img_file:
    pdf_path = os.path.join(tmp_dir, pdf_img_file.name)
    with open(pdf_path, "wb") as f:
        f.write(pdf_img_file.getbuffer())
    images = convert_from_path(pdf_path)
    img_files = []
    for i, img in enumerate(images):
        img_path = os.path.join(tmp_dir, f"page_{i+1}.jpg")
        img.save(img_path, "JPEG")
        img_files.append(img_path)
    st.success(f"PDF converted to {len(images)} image(s)!")
    for img_file in img_files:
        st.image(img_file, use_column_width=True)
        st.download_button(f"Download {os.path.basename(img_file)}", img_file, os.path.basename(img_file))

# -----------------------
# Images → PDF
# -----------------------
st.header("Images → PDF")
img_files = st.file_uploader("Upload images (JPG/PNG) to merge into PDF", type=["jpg","jpeg","png"], accept_multiple_files=True, key="img2pdf")
if img_files:
    pdf_output = os.path.join(tmp_dir, "merged.pdf")
    pdf = FPDF()
    for img_file in img_files:
        image = Image.open(img_file)
        pdf.add_page()
        pdf.image(img_file, x=0, y=0, w=210, h=297)
    pdf.output(pdf_output)
    st.success("Images merged into PDF successfully!")
    st.download_button("Download PDF", pdf_output, "merged.pdf")

# -----------------------
# Merge PDFs
# -----------------------
st.header("Merge PDFs")
merge_pdfs = st.file_uploader("Upload PDFs to merge", type="pdf", accept_multiple_files=True, key="mergepdf")
if merge_pdfs:
    merger = PdfMerger()
    for pdf_file in merge_pdfs:
        merger.append(pdf_file)
    merged_output = os.path.join(tmp_dir, "merged_output.pdf")
    merger.write(merged_output)
    merger.close()
    st.success("PDFs merged successfully!")
    st.download_button("Download Merged PDF", merged_output, "merged.pdf")

# -----------------------
# Split PDF
# -----------------------
st.header("Split PDF")
split_pdf_file = st.file_uploader("Upload PDF to split", type="pdf", key="splitpdf")
if split_pdf_file:
    reader = PdfReader(split_pdf_file)
    num_pages = len(reader.pages)
    st.write(f"Total Pages: {num_pages}")
    start_page = st.number_input("Start Page", min_value=1, max_value=num_pages, value=1)
    end_page = st.number_input("End Page", min_value=1, max_value=num_pages, value=num_pages)
    if st.button("Split PDF"):
        writer = PdfWriter()
        for i in range(start_page-1, end_page):
            writer.add_page(reader.pages[i])
        split_output = os.path.join(tmp_dir, f"split_{split_pdf_file.name}")
        with open(split_output, "wb") as f:
            writer.write(f)
        st.success("PDF split successfully!")
        st.download_button("Download Split PDF", split_output, f"split_{split_pdf_file.name}")
