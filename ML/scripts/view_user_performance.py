import sqlite3

DB_PATH = "data/mcq_database.db"

def view_user_performance():
    """Fetches and displays user performance records."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT up.user_id, u.username, q.question, up.user_answer, q.correct_answer, 
           CASE WHEN up.user_answer = q.correct_answer THEN '✅ Correct' ELSE '❌ Incorrect' END AS result, 
           up.timestamp
    FROM user_performance up
    JOIN users u ON up.user_id = u.id
    JOIN questions q ON up.question_id = q.id
    ORDER BY up.timestamp DESC
    """)
    
    performance_records = cursor.fetchall()
    conn.close()

    if not performance_records:
        print("No user performance data found.")
        return

    print("\n📊 **User Performance Records:**\n")
    for record in performance_records:
        user_id, username, question, user_answer, correct_answer, result, timestamp = record
        print(f"👤 **User:** {username} (ID: {user_id})")
        print(f"📝 **Question:** {question}")
        print(f"❓ **User's Answer:** {user_answer}")
        print(f"✅ **Correct Answer:** {correct_answer}")
        print(f"📌 **Result:** {result}")
        print(f"📅 **Attempted On:** {timestamp}\n" + "-"*50)

if __name__ == "__main__":
    view_user_performance()