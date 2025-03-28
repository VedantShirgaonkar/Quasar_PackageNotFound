from flask import Flask, request, jsonify, render_template,session, redirect, url_for, make_response
from user import register_user, login_user
from datetime import timedelta
import uuid
from database import get_db_connection
import html
import ast
import sqlite3
import sys,os



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Gemma_2.mcq_generator import generateMCQ,convertToJSON


# Dependencies for the PDF processing
import io
import pdfplumber

from Backend.mcq_generator import generate_mcq  # Your MCQ generator function
from Backend.text_processing import extract_text  # Your text extraction function
from Backend.key_sentence_extraction import extract_key_sentences

app = Flask(__name__)
app.secret_key = 'quizgenius'
app.permanent_session_lifetime = timedelta(minutes=120)

session_store = {}

@app.route('/')
def landing_page():
    return render_template('Landing.html')


@app.route('/teacher_dashboard')
def teacher_dashboard():
    return render_template('teacher_dashboard.html')


@app.route('/classes1')
def classroom():
    return render_template('classes1.html')

# @app.route('/classes1')
# def classroom():
#     return render_template('classes1.html')


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username'].lower()
    password = data['password']
    confirm_password = data['confirmPassword']
    role  = data['role']

    if register_user(username, password, confirm_password,role):
        print("User registered successfull")
       # return jsonify({"message": "User registered successfully!"}),200

    else:
        print('Error: User registration failed!')
        return jsonify({"message": "Error: User registration failed!"}), 400


@app.route('/teacher_question')
def teacher_question():
    return render_template('teacher_question.html')
    
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']


    if login_user(username, password):
        session.permanent = True
        uid = str(uuid.uuid4())
        session['session_id'] = uid
        session_store[uid] = username
        print("User Login successfull")
        print(session_store)
        response = make_response(jsonify({"message": "User login successfully!"}), 200)
        response.set_cookie('session_id', session['session_id'], httponly=True,max_age=120*60)
        return response
    else:
        print('Error: User login failed!')
        return jsonify({"message": "Error: User login failed!"}), 400

@app.route('/Student_dashboard')
def Student_dashboard():
    session_id = request.cookies.get('session_id')
    if session_id != session.get('session_id'):
            return redirect(url_for('/'))
    else:
        username = session_store[session_id]
        return render_template('Student_dashboard.html', username=username)
         

@app.route('/question_config')
def question_config():
    session_id = request.cookies.get('session_id')
    if session_id != session.get('session_id'):
            return redirect(url_for('/'))
    else:
        username = session_store[session_id]
        return render_template('question_config.html', username=username)

def executePDF(pdfFileName):
    session_id = session.get('session_id')  # Use get() to prevent KeyError
    if not session_id:
        return jsonify({"error": "Session ID not found"}), 400  # Handle missing session

    username = session_store.get(session_id)
    if not username:
        return jsonify({"error": "User not found in session"}), 400  # Handle missing user

    # sqlUserName = f"SELECT id FROM users WHERE username='{username}'"
    conn = get_db_connection()
    cursor = conn.cursor()

    sqlUserName = "SELECT id FROM users WHERE username='"+session_store[session['session_id']]+"'"
    cursor.execute(sqlUserName)

    user_id = cursor.fetchone()[0]
    filePath=f"files/data/{pdfFileName}"
    print(filePath)
    extracted_text = extract_text(filePath)
    print(extracted_text)
    # key_sentences = extract_key_sentences(extracted_text.split("."))
    # Generate MCQs from extracted text
    # Insert data into the database
    mcqs = generate_mcq(extracted_text,"Medium")  
    print(mcqs)
    insert_questions_into_db(sqlUserName,"Input-Based",mcqs)
    
    return jsonify({"status": "done"}) , 200
        # conn = get_db_connection()
        # cursor = conn.cursor()
        # sql_statement = "SELECT COUNT(*) FROM questions WHERE domain = '"+domain+"'"
        # cursor.execute(sql_statement)
        # count = cursor.fetchone()[0]  # Extract the count value
    
    

@app.route('/checkmcqdone', methods=['POST'])
def checkmcqdone():
    data = request.get_json()
    print(data)
    domain = data['domain']
    numOfQuestions=data['numQuestions'] 
    if domain == '':
        domain = "AI in Healthcare"
        numOfQuestions=10
        # Shifting the Session Domain Value
        # session['domain']=domain
        # pdfFileName = data['pdf_filename']
        # return executePDF(pdfFileName)
        # # Don't return the values wait for the above method to return a value
    

    session['domain']=domain   
    print(data['pdf_filename'])
    # call llm code with variable domain
    # if llm code returns true then return jsonify({"status": "done"}), 200
    mcq_text=generateMCQ(domain,numOfQuestions)
    jsonFormat=convertToJSON(mcq_text,"sampleGeneration.json")

    # Connecting with the db to fetch the username 
    conn = get_db_connection()
    cursor = conn.cursor()

    sqlUserName = "SELECT id FROM users WHERE username='"+session_store[session['session_id']]+"'"
    cursor.execute(sqlUserName)
    user_id = cursor.fetchone()[0]

    # inserting the values into the database by calling that functions
    insert_questions_into_db(user_id,domain,jsonFormat)

    conn = get_db_connection()
    cursor = conn.cursor()
    sql_statement = "SELECT COUNT(*) FROM questions WHERE domain = '"+domain+"'"
    cursor.execute(sql_statement)
    count = cursor.fetchone()[0]  # Extract the count value
    
    # Check if count is greater than or equal to 10
    if count >= 10:
        print("Count is greater than or equal to 10")
        return jsonify({"status": "done"}), 200
    else:
        print("Count is less than 10")
        return jsonify({"status": "notdone"}), 400
    
''' session_id = request.cookies.get('session_id')
    if session_id != session.get('session_id'):
            return redirect(url_for('/'))
    else:
        username = session_store[session_id]
        return jsonify({"status": "done"}), 200'''

# Function for the Database Entries 
# Function to insert questions into the database
def insert_questions_into_db(user_id,domain, mcq_list):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect("quizgenius.db")
        cursor = conn.cursor()
        
        # Insert each question into the table
        for mcq in mcq_list:
            cursor.execute('''
        INSERT INTO questions (user_id, domain, difficulty, question, A, B, C, D, correct_answer)
        VALUES (?, ?, 'Medium', ?, ?, ?, ?, ?, ?)
    ''', (user_id, domain, mcq["question"], mcq["A"], mcq["B"], mcq["C"], mcq["D"], mcq["answer"]))

        # Commit and close the connection
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Database Error:", e)
        return False

import html
from flask import Flask, render_template

@app.route('/showmcq', methods=['POST', 'GET'])
def showmcq():
    # data = request.get_json()
    # domain = data['domain']
    conn = get_db_connection()
    cursor = conn.cursor()
    domain=session['domain']

    # Domain is input-based for now (where we are uploading the pdf file)
    sql_statement = "SELECT id, question, A, B, C, D FROM questions WHERE domain = '"+domain+"' LIMIT 10"
    cursor.execute(sql_statement)
    questions = cursor.fetchall()
    print(questions)

    # Unescape special characters in each string field
    unescaped_questions = [
        (q[0], html.unescape(q[1]), html.unescape(q[2]), html.unescape(q[3]), html.unescape(q[4]), html.unescape(q[5])) 
        for q in questions
    ]

    print(unescaped_questions)
    return render_template('mcq_html.html', questions=unescaped_questions)
    # return jsonify({"questions": questions}), 200

@app.route('/submitmcq', methods=['POST'])
def submitmcq():
    data = request.get_json()
    print(data['answer'])
    answer = data['answer']
    answer_dict = ast.literal_eval(answer)
    diff = data['diff']

    for key, value in answer_dict.items():
        print(f"Key: {key}, Value: {value}")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if(value == '0'):
            real_value = 'A'
        if(value == '1'):
            real_value = 'B'
        if(value == '2'):
            real_value = 'C'
        else:
            real_value = 'D'
        #print(session_store[session['session_id']])
        #print(session['session_id'])
        sql_statement = "SELECT id FROM users WHERE username='"+session_store[session['session_id']]+"'"
        cursor.execute(sql_statement)
        user_id = cursor.fetchone()[0]
        #print(user_id)

        sql_statement = "SELECT correct_answer FROM questions WHERE id="+key
        cursor.execute(sql_statement)
        correct_ans = cursor.fetchone()[0]
        #print(correct_ans)
        cursor.execute('''
        INSERT INTO user_performance (user_id, question_id, user_answer, correct,time_diff) VALUES (?, ?, ?, ?,?)
        ''', (user_id, key, real_value, correct_ans, diff))
        conn.commit()
        conn.close()
        return jsonify({"status": "done"}), 200
    

@app.route('/evaluation1', methods=['POST','GET'])
def evaluation():
     return render_template('evaluation1.html')
    
    ##return jsonify({"message": "MCQ submitted successfully!"}), 200


# Upload api for storing the pdf file 
@app.route("/upload", methods=["POST"])
def upload_pdf():
    """Processes a PDF file directly from memory without saving."""
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    domain=session['domain']
    # get the user_id from the session and hardcode the difficulty level
      # Connecting with the db to fetch the username 
    conn = get_db_connection()
    cursor = conn.cursor()
    sqlUserName = "SELECT id FROM users WHERE username='"+session_store[session['session_id']]+"'"
    cursor.execute(sqlUserName)
    user_id = cursor.fetchone()[0]

    pdf_file = request.files["pdf"]  # Get the uploaded file

    # Read PDF as byte stream
    pdf_stream = io.BytesIO(pdf_file.read())  

    # Extract text directly from the byte stream
    extracted_text = extract_text(pdf_stream)
    # Generate MCQs from extracted text
    # Insert data into the database
    mcqs = generate_mcq(extracted_text, user_id, domain="Input-Based")  
    insert_questions_into_db(sqlUserName,'Input-Based',mcqs)
    
    return jsonify ({"status":"done"}) , 200
    




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000,debug=True)