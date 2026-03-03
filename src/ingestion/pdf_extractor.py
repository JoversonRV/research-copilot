# src/ingestion/pdf_extractor.py
import re
import os
import fitz  # PyMuPDF


def _parse_year(creation_date: str) -> int | None:
    """Extract 4-digit year from PDF creationDate string (e.g. 'D:20200909...')."""
    match = re.search(r'(\d{4})', creation_date or "")
    return int(match.group(1)) if match else None


def _paper_id_from_path(pdf_path: str) -> str:
    """Derive a clean paper_id slug from the filename."""
    stem = os.path.splitext(os.path.basename(pdf_path))[0]
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', stem).strip('_').lower()
    return slug


def extract_text_from_pdf(pdf_path: str) -> dict:
    """
    Extract text and metadata from a PDF file.

    Returns:
        dict with keys: text, metadata, pages, extraction_warnings
    """
    doc = fitz.open(pdf_path)

    full_text = ""
    pages = []
    warnings = []

    for page_num, page in enumerate(doc):
        text = page.get_text()
        pages.append({
            "page_number": page_num + 1,
            "text": text,
            "char_count": len(text)
        })
        full_text += f"\n[PAGE {page_num + 1}]\n{text}"

    # Raw PDF metadata
    raw_meta = doc.metadata

    # Structured metadata ready for chunker / vectorstore
    structured_metadata = {
        "paper_id":    _paper_id_from_path(pdf_path),
        "paper_title": raw_meta.get("title", "").strip() or os.path.splitext(os.path.basename(pdf_path))[0],
        "authors":     raw_meta.get("author", "").strip() or "Unknown",
        "year":        _parse_year(raw_meta.get("creationDate", "")),
        "source_file": os.path.basename(pdf_path),
    }

    return {
        "text": full_text,
        "metadata": structured_metadata,
        "raw_metadata": raw_meta,
        "pages": pages,
        "total_pages": len(doc),
        "extraction_warnings": warnings
    }
