# Remove the self-import to break the circular dependency
import sqlite3
import os

DB_PATH = "storage/mcq_data.db"

def create_tables():
    """Creates necessary tables in the MCQ database if they do not exist."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Table for storing MCQs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mcqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                difficulty TEXT NOT NULL
            )
        ''')

        # Index for optimizing queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_difficulty ON mcqs (difficulty)')

        # Table for user difficulty levels
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_difficulty (
                user_id INTEGER PRIMARY KEY,
                difficulty REAL NOT NULL
            )
        ''')

        conn.commit()

def store_mcq(question, options, correct_answer, difficulty):
    """Stores a generated MCQ in the database correctly."""
    if not (question and options and correct_answer):  # Prevent empty MCQs
        print("❌ Error: Incomplete MCQ, skipping database insertion!")
        return
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mcqs (question, option_a, option_b, option_c, option_d, correct_answer, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (question, options[0], options[1], options[2], options[3], correct_answer, difficulty))
        conn.commit()

def update_mcq_difficulty(mcq_id, new_difficulty):
    """Updates the difficulty of a specific MCQ in the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE mcqs
            SET difficulty = ?
            WHERE id = ?
        ''', (new_difficulty, mcq_id))
        conn.commit()

# Ensure tables exist when the script runs
if __name__ == "__main__":
    create_tables()
    print("✅ Database tables ensured (MCQs + User Difficulty).")