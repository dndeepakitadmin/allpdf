from pdf2docx import Converter

def pdf_to_word(input_pdf, output_docx):
    cv = Converter(input_pdf)
    cv.convert(output_docx, start=0, end=None)
    cv.close()
    return output_docx

