import img2pdf

def jpg_to_pdf(jpg_files, output_pdf):
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(jpg_files))
    return output_pdf

