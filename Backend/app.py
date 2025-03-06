from flask import Flask, request, jsonify, render_template,session, redirect, url_for, make_response
from user import register_user, login_user
from datetime import timedelta
import uuid
from database import get_db_connection
import html

app = Flask(__name__)
app.secret_key = 'quizgenius'
app.permanent_session_lifetime = timedelta(minutes=120)

session_store = {}

@app.route('/')
def landing_page():
    return render_template('Landing.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username'].lower()
    password = data['password']
    confirm_password = data['confirmPassword']
    role  = data['role']

    if register_user(username, password, confirm_password,role):
        print("User registered successfull")
        return jsonify({"message": "User registered successfully!"}),200
    else:
        print('Error: User registration failed!')
        return jsonify({"message": "Error: User registration failed!"}), 400
    
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

@app.route('/checkmcqdone', methods=['POST'])
def checkmcqdone():
    conn = get_db_connection()
    cursor = conn.cursor()
    sql_statement = "SELECT COUNT(*) FROM questions WHERE domain = 'Input-Based'"
    cursor.execute(sql_statement)
    count = cursor.fetchone()[0]  # Extract the count value

# Check if count is greater than or equal to 10
    if count >= 3:
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

import html
from flask import Flask, render_template

@app.route('/showmcq', methods=['POST', 'GET'])
def showmcq():
    conn = get_db_connection()
    cursor = conn.cursor()
    sql_statement = "SELECT id, question, A, B, C, D FROM questions WHERE domain = 'Input-Based'"
    cursor.execute(sql_statement)
    questions = cursor.fetchall()

    # Unescape special characters in each string field
    unescaped_questions = [
        (q[0], html.unescape(q[1]), html.unescape(q[2]), html.unescape(q[3]), html.unescape(q[4]), html.unescape(q[5])) 
        for q in questions
    ]

    print(unescaped_questions)
    return render_template('mcq_html.html', questions=unescaped_questions)
    #return jsonify({"questions": questions}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
