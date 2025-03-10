from flask import Flask, request, jsonify, session
from werkzeug.utils import secure_filename
import os
import io
import tempfile
from datetime import timedelta
from text_processing import extract_text_from_pdf
from mcq_generator import generate_mcq
from database import get_db_connection, insert_questions_into_db

app = Flask(__name__)
app.secret_key = 'quizgenius'
app.permanent_session_lifetime = timedelta(minutes=120)
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

# Main Integration Endpoint
@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    # Validate inputs
    if not request.form.get('domain') and 'pdf' not in request.files:
        return jsonify({"error": "Domain selection or PDF upload required"}), 400

    # Get user session
    session_id = request.cookies.get('session_id')
    if not session_id or session_id != session.get('session_id'):
        return jsonify({"error": "Unauthorized"}), 401

    # Process inputs
    try:
        num_questions = int(request.form.get('num_questions', 10))
        domain = request.form.get('domain', 'general')
        difficulty = request.form.get('difficulty', 'medium')
        text = ''

        # PDF Processing
        if 'pdf' in request.files and request.files['pdf'].filename:
            pdf_file = request.files['pdf']
            pdf_stream = io.BytesIO(pdf_file.read())
            text = extract_text_from_pdf(pdf_stream)

        # Generate MCQs
        conn = get_db_connection()
        user_id = conn.execute(
            "SELECT id FROM users WHERE username = ?",
            [session['username']]
        ).fetchone()[0]

        mcqs = generate_mcq(
            text=text,
            user_id=user_id,
            domain=domain,
            difficulty=difficulty,
            num_questions=num_questions
        )

        # Store in database
        if mcqs:
            inserted = insert_questions_into_db(
                user_id=user_id,
                domain=domain,
                mcq_list=mcqs,
                difficulty=difficulty
            )
            if not inserted:
                raise Exception("Failed to store questions")

        return jsonify({"questions": mcqs})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
