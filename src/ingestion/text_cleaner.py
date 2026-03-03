# src/ingestion/text_cleaner.py
import re

def clean_extracted_text(text: str) -> str:
    """Clean and normalize extracted PDF text."""

    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    # Fix hyphenated words at line breaks
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)

    # Remove page numbers and headers (customize per document)
    text = re.sub(r'\n\d+\n', '\n', text)

    # Normalize quotes
    text = text.replace('\u201c', '"').replace('\u201d', '"')

    return text.strip()
