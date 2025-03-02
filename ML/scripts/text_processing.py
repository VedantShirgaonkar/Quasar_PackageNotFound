from PyPDF2 import PdfReader
import spacy
import re
import os

def clean_text(text):
    """Cleans text by fixing spacing, removing unwanted characters, and standardizing formatting."""
    text = re.sub(r'\n+', ' ', text)  # Replace multiple new lines with a space
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    text = re.sub(r'[^a-zA-Z0-9.,?!"\'\-:/() ]+', '', text)  # Keep essential characters
    text = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', text)  # Add space between numbers & words (e.g., "2025Hackathon" → "2025 Hackathon")
    text = re.sub(r'([a-zA-Z])(\d+)', r'\1 \2', text)  # Add space between words & numbers (e.g., "AIbased" → "AI based")
    text = re.sub(r'(\w)-(\w)', r'\1\2', text)  # Preserve hyphenated words
    text = re.sub(r'\b(?:Figure|Table)\s+\d+[.:]', '', text)  # Remove figure references
    return text

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file, handling missing text cases."""
    try:
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            text = ' '.join([page.extract_text() or '' for page in reader.pages])  # Handle NoneType
        return text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""

def extract_text_from_txt(txt_path):
    """Reads text from a .txt file."""
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading text file: {e}")
        return ""

def process_input(file_path):
    """Extracts, cleans, and segments text from PDF or text file."""
    nlp = spacy.load("en_core_web_sm")

    # Read text based on file type
    if file_path.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".txt"):
        raw_text = extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file format. Use .pdf or .txt")

    cleaned_text = clean_text(raw_text)

    # Process with spaCy for sentence segmentation
    doc = nlp(cleaned_text)
    key_sentences = [clean_text(sent.text) for sent in doc.sents if len(sent.text.split()) > 5]  # Filter short sentences

    return key_sentences

# Test the module independently
if __name__ == "__main__":
    test_file = "data/Hack the Future.pdf"  # Change this to an actual file path
    if os.path.exists(test_file):
        sentences = process_input(test_file)
        print("\n🔹 Extracted Sentences:")
        for i, sentence in enumerate(sentences, 1):
            print(f"{i}. {sentence}")
    else:
        print("❌ Test file not found! Please provide a valid path.")