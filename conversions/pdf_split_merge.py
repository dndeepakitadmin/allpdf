from PyPDF2 import PdfMerger, PdfReader, PdfWriter

def merge_pdfs(pdf_list, output_pdf):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_pdf)
    merger.close()
    return output_pdf

def split_pdf(input_pdf, output_folder):
    reader = PdfReader(input_pdf)
    output_files = []
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        out_path = f"{output_folder}/page_{i+1}.pdf"
        with open(out_path, "wb") as f:
            writer.write(f)
        output_files.append(out_path)
    return output_files

