import sqlite3
import hashlib
import os

# Define the database path
DB_PATH = os.path.join(os.path.dirname(__file__), "quizgenius.db")

# ------------------ DATABASE INITIALIZATION ------------------

def get_db_connection():
    """Creates and returns a connection to the database."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def initialize_database():
    """Creates required tables if they don't already exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table (For authentication & user tracking)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'student',
        difficulty INTEGER DEFAULT 1,  -- 0 (Easy), 1 (Medium), 2 (Hard)
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Questions Table (Stores MCQs)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, 
        domain TEXT NOT NULL, 
        difficulty TEXT DEFAULT 'Medium', 
        question TEXT NOT NULL,
        A TEXT NOT NULL,
        B TEXT NOT NULL,
        C TEXT NOT NULL,
        D TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # User Performance Table (Tracks quiz results)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        user_answer TEXT NOT NULL,
        correct BOOLEAN NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

# ------------------ USER AUTHENTICATION ------------------

def hash_password(password):
    """Hashes password using SHA-256 for security."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password, role="student"):
    """Registers a new user with a hashed password."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hashed_password, role))
        conn.commit()
        print(f"✅ User '{username}' registered successfully.")
    except sqlite3.IntegrityError:
        print(f"❌ Username '{username}' already exists.")
    
    conn.close()

def get_user_id(username, password):
    """Retrieves user ID if credentials match."""
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()

    return user[0] if user else None

# ------------------ MCQ STORAGE & RETRIEVAL ------------------

def store_mcq(user_id, domain, question_data):
    """Stores a generated MCQ into the database, preventing duplicates."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the question already exists for this user
    cursor.execute("SELECT id FROM questions WHERE question = ? AND user_id = ?", (question_data["question"], user_id))
    # Insert the new question if it's not a duplicate
    cursor.execute("""
    INSERT INTO questions (user_id, domain, difficulty, question, A, B, C, D, correct_answer)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, 
        domain, 
        question_data["difficulty"], 
        question_data["question"], 
        question_data["options"]["A"], 
        question_data["options"]["B"], 
        question_data["options"]["C"], 
        question_data["options"]["D"], 
        question_data["answer"]
    ))
    
    question_id = cursor.lastrowid  # Get the newly inserted question ID
    conn.commit()
    conn.close()
    return question_id  # Return the ID for use in performance tracking

def get_user_performance(user_id):
    """Fetches user performance data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            SUM(CASE WHEN correct = 1 THEN 1 ELSE 0 END),
            SUM(CASE WHEN correct = 0 THEN 1 ELSE 0 END)
        FROM user_performance
        WHERE user_id = ?
    """, (user_id,))
    
    correct_count, incorrect_count = cursor.fetchone() or (0, 0)
    conn.close()
    return correct_count, incorrect_count

def store_user_performance(user_id, question_id, user_answer, correct):
    """Logs user responses for adaptive learning."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO user_performance (user_id, question_id, user_answer, correct)
        VALUES (?, ?, ?, ?)
        """, (user_id, question_id, user_answer, correct))
        
        conn.commit()
        print(f"✅ User performance recorded successfully for Question ID: {question_id}")
    
    finally:
        conn.close()

# Initialize the database when the script is loaded
initialize_database()