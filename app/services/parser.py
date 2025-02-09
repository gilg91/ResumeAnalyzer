from pdfminer.high_level import extract_text
from docx import Document
import os

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    return extract_text(file_path)

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_resume_text(file_path: str) -> str:
    """Extract text based on file type."""
    _, ext = os.path.splitext(file_path)
    
    if ext.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext.lower() == ".docx":
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format"
