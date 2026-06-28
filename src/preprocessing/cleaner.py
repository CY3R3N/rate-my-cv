# src/preprocessing/cleaner.py

import re

def clean_text(text: str) -> str:
    """Clean raw resume text extracted from PDF/DOCX."""
    
    # Normalize unicode characters instead of stripping them
    import unicodedata
    text = unicodedata.normalize('NFKC', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text