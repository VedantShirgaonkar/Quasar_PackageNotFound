from flask import Flask, request, jsonify
import io
import pdfplumber
from scripts.mcq_generator import generate_mcq  # Your MCQ generator function
from scripts.text_processing import extract_text  # Your text extraction function

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_pdf():
    """Processes a PDF file directly from memory without saving."""
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["pdf"]  # Get the uploaded file

    # Read PDF as byte stream
    pdf_stream = io.BytesIO(pdf_file.read())  

    # Extract text directly from the byte stream
    extracted_text = extract_text(pdf_stream)  

    # Generate MCQs from extracted text
    mcqs = generate_mcq(extracted_text, user_id=1, domain="Input-Based")  # Example user_id

    return jsonify({"message": "PDF processed successfully", "mcqs": mcqs})

if __name__ == "__main__":
    app.run(debug=True)