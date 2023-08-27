from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
import pandas as pd
import os
import io

def modify_pdf(pdf_filename, xlsx_filename, app):
    df = pd.read_excel(os.path.join(app.root_path, xlsx_filename))
    names = df['names'].tolist()
    dates = df['dates'].tolist()
    
    page_width, page_height = letter
    
    font_name = "Helvetica-Bold"  # Default font
    font_size = 26  # Default size
    
    existing_pdf = PdfReader(open(os.path.join(app.root_path, pdf_filename), "rb"))
    page = existing_pdf.pages[0]
    page_width = page.mediabox[2]  # upper-right x-coordinate
    page_height = page.mediabox[3]  # upper-right y-coordinate

    for i in range(len(names)):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        can.setFont(font_name, font_size)
        
        center_of_canvas = page_width / 2
        half_text_width = stringWidth(names[i], font_name, font_size) / 2
        x = center_of_canvas - half_text_width
                
        can.drawString(x, 250, names[i])  # Modify these values to change the position of the name
        can.setFont("Helvetica-Bold", 16)
        can.drawString(128, 85, str(dates[i]))  # Modify these values to change the position of the date
        can.save()

        packet.seek(0)
        new_pdf = PdfReader(packet)
        existing_pdf = PdfReader(open(os.path.join(app.root_path, pdf_filename), "rb"))
        output = PdfWriter()

        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)  # Updated this line

        output_filename = f"{names[i]}_{dates[i]}.pdf"
        with open(os.path.join(app.root_path, output_filename), "wb") as output_pdf:
            output.write(output_pdf)
