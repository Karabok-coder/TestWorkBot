from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from io import BytesIO

from bot.data.config import PATH_FONT

async def generate_pdf(data):
    pdfmetrics.registerFont(TTFont('Arial', PATH_FONT))

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    c.setFont('Arial', 12)

    y = 750
    for key, value in data.items():
        text = f"{key}: {value}"
        c.drawString(100, y, text)
        y -= 20
    
    c.save()
    
    buffer.seek(0)
    pdf_bytes = buffer.getvalue()
    
    return pdf_bytes