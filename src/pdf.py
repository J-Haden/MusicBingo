from pathlib import Path
import subprocess
from pypdf import PdfWriter
import os

LIBREOFFICE_PATH = os.getenv('LIBREOFFICE_PATH', 'libreoffice')

def convert_excel_to_pdf(excel_file, output_folder):
    excel_file = Path(excel_file)
    output_folder = Path(output_folder)
    
    subprocess.run(
        [
            LIBREOFFICE_PATH,
            '--headless',
            '--convert-to',
            'pdf',
            '--outdir',
            str(output_folder),
            str(excel_file)
        ], 
        check=True
    )
    
    return output_folder/f'{excel_file.stem}.pdf'

def merge_pdfs(pdf_files, output_file):
    
    writer = PdfWriter()
    
    for pdf in pdf_files:
        writer.append(pdf)
    
    with open(output_file, 'wb') as f:
        writer.write(f)