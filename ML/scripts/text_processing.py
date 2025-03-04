import re
import spacy
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """Cleans text by removing unwanted characters and ensuring proper sentence structure."""
    text = re.sub(r'\n+', ' ', text)  # Replace multiple new lines with spaces
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    text = re.sub(r'[^a-zA-Z0-9.,?!"\'\-:/() ]+', '', text)  # Keep only useful characters
    return text

def extract_text(pdf_path):
    """Extracts text from a PDF file and restructures it into full sentences."""
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        text = ' '.join([page.extract_text() or '' for page in reader.pages])

    text = clean_text(text)

    # Process with spaCy for sentence segmentation
    doc = nlp(text)
    structured_sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.split()) > 5]

    return structured_sentences

if __name__ == "__main__":
    test_file = "data/sample.pdf"
    sentences = extract_text(test_file)

    print("\n🔹 Preprocessed Sentences:")
    for i, sentence in enumerate(sentences, 1):
        print(f"{i}. {sentence}")