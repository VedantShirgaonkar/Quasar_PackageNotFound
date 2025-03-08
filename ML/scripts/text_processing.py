import fitz  # PyMuPDF for text extraction
import pdfplumber  # Extract text from PDFs
import pytesseract  # OCR for scanned PDFs
from PIL import Image
import io

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF using multiple methods:
    1. pdfplumber (Preferred for structured PDFs)
    2. PyMuPDF (Fallback for extracting raw text)
    3. OCR via pytesseract (Last resort for scanned PDFs)
    """
    # Try extracting text using pdfplumber (works best for structured PDFs)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages).strip()
            if text:
                return text  # Return if successful
    except Exception:
        pass  # Ignore errors and try other methods

    # Fallback: Use PyMuPDF to extract raw text
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text("text") for page in doc).strip()
        if text:
            return text  # Return if successful
    except Exception:
        pass  # Ignore errors and try OCR

    # Last resort: Use OCR for scanned PDFs
    try:
        with fitz.open(pdf_path) as doc:
            text = "\n".join(
                pytesseract.image_to_string(Image.open(io.BytesIO(page.get_pixmap().tobytes())))
                for page in doc
            ).strip()
            return text
    except Exception:
        return ""  # If all methods fail, return an empty string

def extract_text(source):
    """
    Extracts text from a given source:
    - If the source is a PDF file, it processes it accordingly.
    - Otherwise, it assumes the source is plain text and returns it as is.
    """
    return extract_text_from_pdf(source) if source.lower().endswith(".pdf") else source.strip()