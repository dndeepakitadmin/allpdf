import streamlit as st
import os
from conversions.pdf_to_word import pdf_to_word
from conversions.word_to_pdf import word_to_pdf
from conversions.pdf_to_jpg import pdf_to_jpg
from conversions.jpg_to_pdf import jpg_to_pdf
from conversions.pdf_split_merge import merge_pdfs, split_pdf
from conversions.excel_pdf import pdf_to_excel, excel_to_pdf
from conversions.deletion_certificate import generate_deletion_certificate

# Temporary storage
TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

st.set_page_config(page_title="AllPDF Converter", layout="wide")
st.title("📄 AllPDF Multi-File Converter")

# --- Checkbox Acknowledgment ---
ack = st.checkbox(
    "I acknowledge that files uploaded will be temporarily processed and deleted after download"
)

if ack:

    # --- Conversion Type ---
    option = st.selectbox(
        "Select Conversion Type",
        [
            "PDF → Word",
            "Word → PDF",
            "PDF → JPG",
            "JPG → PDF",
            "PDF Split",
            "PDF Merge",
            "PDF → Excel",
            "Excel → PDF"
        ]
    )

    # --- File Upload ---
    uploaded_files = st.file_uploader(
        "Upload your file(s) (Max 200 MB per file)",
        type=["pdf","docx","jpg","xlsx","csv"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("Convert"):

        converted_files = []

        for uploaded_file in uploaded_files:

            if uploaded_file.size > 200 * 1024 * 1024:
                st.error(f"{uploaded_file.name} exceeds 200 MB limit.")
                continue

            file_path = os.path.join(TEMP_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            try:
                # --- Conversion Logic ---
                if option == "PDF → Word":
                    output_file = file_path.replace(".pdf", ".docx")
                    pdf_to_word(file_path, output_file)
                    converted_files.append(output_file)

                elif option == "Word → PDF":
                    output_file = file_path.replace(".docx", ".pdf")
                    word_to_pdf(file_path, output_file)
                    converted_files.append(output_file)

                elif option == "PDF → JPG":
                    output_files = pdf_to_jpg(file_path, TEMP_DIR)
                    for f in output_files:
                        st.download_button(
                            "Download " + os.path.basename(f),
                            open(f, "rb"),
                            file_name=os.path.basename(f)
                        )
                    continue

                elif option == "JPG → PDF":
                    output_file = file_path.replace(".jpg", ".pdf")
                    jpg_to_pdf([file_path], output_file)
                    converted_files.append(output_file)

                elif option == "PDF Split":
                    output_files = split_pdf(file_path, TEMP_DIR)
                    for f in output_files:
                        st.download_button(
                            "Download " + os.path.basename(f),
                            open(f, "rb"),
                            file_name=os.path.basename(f)
                        )
                    continue

                elif option == "PDF Merge":
                    if len(uploaded_files) < 2:
                        st.error("Select at least 2 PDFs to merge.")
                        continue
                    merge_list = [os.path.join(TEMP_DIR, f.name) for f in uploaded_files]
                    output_file = os.path.join(TEMP_DIR, "merged.pdf")
                    merge_pdfs(merge_list, output_file)
                    converted_files.append(output_file)

                elif option == "PDF → Excel":
                    output_file = file_path.replace(".pdf", ".csv")
                    pdf_to_excel(file_path, output_file)
                    converted_files.append(output_file)

                elif option == "Excel → PDF":
                    output_file = file_path.replace(".xlsx", ".pdf")
                    excel_to_pdf(file_path, output_file)
                    converted_files.append(output_file)

                else:
                    st.error("Option not implemented.")
                    continue

            except Exception as e:
                st.error(f"Error converting {uploaded_file.name}: {e}")

        # --- Download Converted Files ---
        for f in converted_files:
            st.download_button(
                "Download " + os.path.basename(f),
                open(f, "rb"),
                file_name=os.path.basename(f)
            )

        # --- Deletion Certificate ---
        if converted_files:
            if st.button("Generate Deletion Certificate"):
                cert_file = generate_deletion_certificate(
                    user_name="Anonymous",
                    files_deleted=[os.path.basename(f) for f in converted_files]
                )
                st.success("Deletion certificate generated!")
                st.download_button(
                    "Download Deletion Certificate",
                    open(cert_file, "rb"),
                    file_name=os.path.basename(cert_file)
                )
