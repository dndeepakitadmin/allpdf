import pandas as pd
import os
import pdfkit

def excel_to_pdf(input_excel, output_pdf):
    df = pd.read_excel(input_excel)
    html_file = output_pdf.replace(".pdf", ".html")
    df.to_html(html_file, index=False)
    pdfkit.from_file(html_file, output_pdf)
    os.remove(html_file)
    return output_pdf

def pdf_to_excel(input_pdf, output_csv):
    import tabula
    tabula.convert_into(input_pdf, output_csv, output_format='csv', pages='all')
    return output_csv

