# src/ingestion/resume_parser.py

import pdfplumber
from docx import Document


def parse_pdf(file_path: str) -> str:
    """Extract text from a PDF resume."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def parse_docx(file_path: str) -> str:
    """Extract text from a DOCX resume."""
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text.strip()


def parse_resume(file_path: str) -> str:
    """Auto-detect format and parse resume."""
    if file_path.endswith(".pdf"):
        return parse_pdf(file_path)
    elif file_path.endswith(".docx"):
        return parse_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Upload a PDF or DOCX.")