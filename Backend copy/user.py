import bcrypt
import sqlite3
from database import get_db_connection

# Function to hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

# Function to verify the entered password with the stored hash
def verify_password(stored_password, entered_password):
    return bcrypt.checkpw(entered_password.encode(), stored_password)

# Function to register a user
def register_user(username, password, confirm_password,role):
    if password != confirm_password:
        print("Error: Passwords do not match!")
        return False

    hashed_password = hash_password(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        sql_statement = "SELECT * FROM users WHERE username = '"+username+"'" 
        cursor.execute(sql_statement)

        user = cursor.fetchone()

        if user:
              print("Error: Username already exists!")
              return False
        
        cursor.execute('''
        INSERT INTO users (username, password,role) VALUES (?, ?, ?)
        ''', (username, hashed_password, role))

        conn.commit()
        print(f"User {username} registered successfully!")
        return True
    except sqlite3.IntegrityError:
        print("Error: Username already exists!")
        return False
    finally:
        conn.close()

# Function to authenticate a user
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    conn.close()

    if user and verify_password(user[0], password):
        print("Login successful!")
        return True
    else:
        print("Invalid username or password!")
        return False
