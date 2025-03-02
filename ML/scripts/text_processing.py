from PyPDF2 import PdfReader
import spacy
import re

def clean_text(text):
    """Removes extra spaces, new lines, and non-alphanumeric characters at the start/end."""
    text = re.sub(r'\n+', ' ', text)  # Replace multiple new lines with space
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    text = re.sub(r'[^a-zA-Z0-9.,?!"\' ]+', '', text)  # Remove special characters except punctuation
    return text

def process_input(file_path):
    """Extracts and cleans text from a PDF or raw text file."""
    nlp = spacy.load("en_core_web_sm")
    
    # Read text from file
    if file_path.endswith('.pdf'):
        text = ''.join([page.extract_text() for page in PdfReader(file_path).pages if page.extract_text()])
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    
    # Clean the extracted text
    cleaned_text = clean_text(text)

    # Process with spaCy
    doc = nlp(cleaned_text)
    key_sentences = [clean_text(sent.text) for sent in doc.sents if len(sent.text.split()) > 5]  # Keep meaningful sentences
    return key_sentences