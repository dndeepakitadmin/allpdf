from pdf2image import convert_from_path
import os

def pdf_to_jpg(input_pdf, output_folder):
    images = convert_from_path(input_pdf)
    output_files = []
    for i, img in enumerate(images):
        out_path = os.path.join(output_folder, f"page_{i+1}.jpg")
        img.save(out_path, "JPEG")
        output_files.append(out_path)
    return output_files

