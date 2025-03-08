from flask import Flask, request
import pdfplumber  # or PyMuPDF (fitz) based on your existing pipeline

app = Flask(__name__)

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']  # Get the uploaded file
    if file.filename == '':
        return "No selected file", 400

    # Read the PDF directly without storing it
    extracted_text = extract_text_from_pdf(file)

    # Pass the extracted text to the MCQ generator
    mcqs = generate_mcq(extracted_text)

    return {"mcqs": mcqs}  # Return generated MCQs as a response

def extract_text_from_pdf(file_obj):
    """Extracts text from an uploaded PDF file without saving it."""
    text = ""
    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

if __name__ == '__main__':
    app.run(debug=True)