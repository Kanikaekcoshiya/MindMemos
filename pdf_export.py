from io import BytesIO
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors

def export_to_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    title_style = styles['Heading1']
    title_style.textColor = colors.HexColor("#1e1e96")
    story.append(Paragraph("MindMemos - Generated Notes", title_style))
    story.append(Spacer(1, 0.3 * inch))

    body_style = styles['Normal']
    for line in text.split("\n"):
        line_stripped = line.strip()
        if not line_stripped:
            story.append(Spacer(1, 0.2 * inch))
            continue
        if line_stripped.endswith(":") or line_stripped.isupper():
            heading_style = styles['Heading3']
            heading_style.textColor = colors.HexColor("#0077cc")
            story.append(Paragraph(line_stripped, heading_style))
        else:
            story.append(Paragraph(line_stripped, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
