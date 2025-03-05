import fitz  # PyMuPDF
import pdfplumber
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(pdf_path):
    """Extracts text from any type of PDF (normal or scanned)."""
    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
    except Exception as e:
        print(f"pdfplumber extraction failed: {e}")

    if not text:
        try:
            # Fallback to PyMuPDF
            doc = fitz.open(pdf_path)
            for page in doc:
                text += page.get_text("text") + "\n"
        except Exception as e:
            print(f"PyMuPDF extraction failed: {e}")

    if not text:
        try:
            # Fallback to OCR for scanned PDFs
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    pix = page.get_pixmap()
                    img = Image.open(io.BytesIO(pix.tobytes()))
                    text += pytesseract.image_to_string(img) + "\n"
        except Exception as e:
            print(f"OCR extraction failed: {e}")

    return text.strip()

def extract_text_from_paragraph(paragraph):
    """Handles direct paragraph input."""
    return paragraph.strip()

def extract_text(source):
    """Universal function that works for PDF, text, or paragraph input."""
    if source.lower().endswith(".pdf"):
        return extract_text_from_pdf(source)
    return extract_text_from_paragraph(source)