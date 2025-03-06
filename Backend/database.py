import sqlite3

# Function to connect to the database
def get_db_connection():
    return sqlite3.connect("quizgenius.db", check_same_thread=False)


def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    question TEXT NOT NULL,
    A TEXT NOT NULL,
    B TEXT NOT NULL,
    C TEXT NOT NULL,
    D TEXT NOT NULL,
    correct_answer TEXT NOT NULL
)
''')

    
    conn.commit()
    conn.close()

create_table()
