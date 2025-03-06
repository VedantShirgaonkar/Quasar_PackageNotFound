import sqlite3

DB_PATH = "data/mcq_database.db"

def view_mcqs():
    """Fetches and displays MCQs from the database in a readable format."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT domain, difficulty, question, A, B, C, D, correct_answer FROM questions")
    mcqs = cursor.fetchall()
    conn.close()

    if not mcqs:
        print("No MCQs found in the database.")
        return

    print("\n📚 **Stored MCQs in Database:**\n")
    for idx, (domain, difficulty, question, A, B, C, D, correct_answer) in enumerate(mcqs, 1):
        print(f"MCQ {idx}: {question}")
        print(f"A) {A}")
        print(f"B) {B}")
        print(f"C) {C}")
        print(f"D) {D}")
        print(f"✅ Correct Answer: {correct_answer}")
        print(f"🔹 Domain: {domain} | 🔹 Difficulty: {difficulty}\n" + "-"*50)

if __name__ == "__main__":
    view_mcqs()