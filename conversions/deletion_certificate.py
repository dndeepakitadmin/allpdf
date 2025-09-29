from fpdf import FPDF
from datetime import datetime

def generate_deletion_certificate(user_name="User", files_deleted=[]):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "File Deletion Certificate", ln=True, align="C")
    
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"This is to certify that the following file(s) uploaded by {user_name} have been deleted from the server:")
    
    for f in files_deleted:
        pdf.cell(0, 10, f"- {f}", ln=True)
    
    pdf.ln(10)
    pdf.cell(0, 10, f"Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    
    output_file = f"temp_files/deletion_certificate_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(output_file)
    return output_file

