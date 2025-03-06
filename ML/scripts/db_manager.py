import sqlite3
import hashlib

DB_PATH = "data/mcq_database.db"

def initialize_database():
    """Creates required tables if they don't already exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

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

def store_mcq(user_id, domain, question_data):
    """Stores a generated MCQ into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
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
    question_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return question_id

def store_user_performance(user_id, question_id, user_answer, correct):
    """Logs user responses for adaptive learning."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO user_performance (user_id, question_id, user_answer, correct)
    VALUES (?, ?, ?, ?)
    """, (user_id, question_id, user_answer, correct))
    conn.commit()
    conn.close()

def hash_password(password):
    """Hashes password using SHA-256 for security."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    """Registers a new user (password is securely hashed)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print(f"✅ User '{username}' registered successfully.")
    except sqlite3.IntegrityError:
        print(f"❌ Username '{username}' already exists.")
    
    conn.close()

def get_user_id(username, password):
    """Retrieves user ID if credentials match."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    hashed_password = hash_password(password)
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()

    return user[0] if user else None