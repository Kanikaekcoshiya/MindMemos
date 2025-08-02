from PyPDF2 import PdfReader
from docx import Document
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

#FILE PROCESSING 
def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file."""
    text = ""
    pdf_reader = PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text.strip()

def extract_text_from_docx(uploaded_file):
    """Extract text from a DOCX file."""
    doc = Document(uploaded_file)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text.strip()

def process_file(uploaded_file, prompt_type, language):
    """Process uploaded file and generate notes in selected language."""
    try:
        # Extract text
        if uploaded_file.name.endswith(".pdf"):
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            text = extract_text_from_docx(uploaded_file)
        else:
            return "⚠️ Unsupported file format."

        if not text:
            return "⚠️ Error: No text could be extracted from the file."

        # Prompt based on type
        if prompt_type == "Summary Notes":
            prompt = f"Summarize the content into a very short summary with 5-6 bullet points in {language}."
        elif prompt_type == "Detailed Notes":
            prompt = f"Create detailed notes with clear headings, sub-headings and bullet points for each concept in {language}."
        elif prompt_type == "Q&A Format":
            prompt = f"Generate 5 important questions and answers (3-4 lines each) in {language}."

        full_prompt = f"{prompt}\n\nContent:\n{text}"
        response = model.generate_content([full_prompt])
        return response.text
    except Exception as e:
        return f"⚠️ Error processing file: {e}"

# EXPORT TO PDF 
def export_to_pdf(text):
    """Generate a PDF using ReportLab."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles['Heading1']
    title_style.textColor = colors.HexColor("#1e1e96")
    story.append(Paragraph("MindMemos - Generated Notes", title_style))
    story.append(Spacer(1, 0.3*inch))

    # Content
    body_style = styles['Normal']
    for line in text.split("\n"):
        line_stripped = line.strip()
        if not line_stripped:
            story.append(Spacer(1, 0.2*inch))
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
