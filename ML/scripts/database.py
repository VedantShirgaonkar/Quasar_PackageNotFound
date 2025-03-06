import sqlite3
import hashlib

DB_FILE = "mcq_database.db"

def connect_db():
    """Connects to SQLite database and returns connection & cursor."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    return conn, cursor

def create_tables():
    """Creates all necessary tables if they don't exist."""
    conn, cursor = connect_db()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,  -- Store hashed password
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        domain TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        question TEXT NOT NULL,
        A TEXT NOT NULL,
        B TEXT NOT NULL,
        C TEXT NOT NULL,
        D TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS user_performance (
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        result TEXT NOT NULL CHECK(result IN ('correct', 'incorrect')),
        attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, question_id),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(question_id) REFERENCES questions(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

def hash_password(password):
    """Returns a hashed version of the password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Registers a new user."""
    conn, cursor = connect_db()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (username, hash_password(password)))
        conn.commit()
        print(f"✅ User '{username}' registered successfully.")
    except sqlite3.IntegrityError:
        print(f"❌ Username '{username}' already exists.")
    finally:
        conn.close()

def authenticate_user(username, password):
    """Authenticates a user based on stored credentials."""
    conn, cursor = connect_db()
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and user[1] == hash_password(password):
        print(f"✅ Welcome, {username}!")
        return user[0]  # Return user ID
    else:
        print("❌ Invalid credentials.")
        return None

def store_mcq(user_id, domain, difficulty, question, options, correct_answer):
    """Stores a generated MCQ into the database."""
    conn, cursor = connect_db()
    cursor.execute("""
        INSERT INTO questions (user_id, domain, difficulty, question, A, B, C, D, correct_answer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, domain, difficulty, question, options["A"], options["B"], options["C"], options["D"], correct_answer))
    conn.commit()
    conn.close()

def store_user_performance(user_id, question_id, result):
    """Stores user's answer correctness for adaptive learning."""
    conn, cursor = connect_db()
    cursor.execute("""
        INSERT INTO user_performance (user_id, question_id, result) 
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, question_id) DO UPDATE SET result = ?
    """, (user_id, question_id, result, result))
    conn.commit()
    conn.close()

def get_user_accuracy(user_id):
    """Calculates user accuracy based on past answers."""
    conn, cursor = connect_db()
    
    cursor.execute("SELECT COUNT(*) FROM user_performance WHERE user_id = ? AND result = 'correct'", (user_id,))
    correct_answers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM user_performance WHERE user_id = ?", (user_id,))
    total_attempts = cursor.fetchone()[0]

    conn.close()

    if total_attempts == 0:
        return 0  # If no attempts, assume 0% accuracy
    
    accuracy = (correct_answers / total_attempts) * 100
    return accuracy

def get_next_difficulty(user_id):
    """Determines the difficulty of the next quiz based on user accuracy."""
    accuracy = get_user_accuracy(user_id)

    if accuracy >= 80:
        return "Hard"
    elif accuracy >= 50:
        return "Medium"
    else:
        return "Easy"