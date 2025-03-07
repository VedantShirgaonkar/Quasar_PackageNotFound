import sqlite3
import json
import ollama
from dbConnection import DB_PATH  # Assuming you have a DB_PATH defined

MODEL_NAME = "gemma:2b"

class AdaptiveLearning:
    def __init__(self, user_id, mode="real-time"):
        """
        Initializes adaptive learning mode.
        mode: 
            - "real-time" → Adjusts difficulty after each question
            - "quiz-based" → Adjusts difficulty after an entire quiz
        """
        self.user_id = user_id
        self.mode = mode
        self.user_difficulty = 1  # 1 (Medium) → 0 (Easy), 2 (Hard)
        self.load_user_difficulty()

    def load_user_difficulty(self):
        """Loads the user's current difficulty level from the database."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT difficulty FROM user_settings WHERE user_id = ?", (self.user_id,))
        row = cursor.fetchone()
        if row:
            self.user_difficulty = row[0]
        conn.close()

    def save_user_difficulty(self):
        """Saves the user's difficulty level in the database."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_settings (user_id, difficulty) 
            VALUES (?, ?) 
            ON CONFLICT(user_id) 
            DO UPDATE SET difficulty=excluded.difficulty
        """, (self.user_id, self.user_difficulty))
        conn.commit()
        conn.close()

    def get_user_performance(self):
        """Fetches the correct and incorrect answer counts for a user."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM user_performance WHERE user_id = ? AND correct = 1", (self.user_id,))
        correct_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM user_performance WHERE user_id = ? AND correct = 0", (self.user_id,))
        incorrect_count = cursor.fetchone()[0]

        conn.close()
        return correct_count, incorrect_count

    def adjust_difficulty_after_mcq(self, last_answer_correct):
        """
        Adjusts difficulty for the *next MCQ* based on the last answer.
        - Increases difficulty if last answer was correct.
        - Decreases difficulty if last answer was incorrect.
        """
        if last_answer_correct:
            self.user_difficulty = min(2, self.user_difficulty + 1)  # Move towards Hard
        else:
            self.user_difficulty = max(0, self.user_difficulty - 1)  # Move towards Easy

        self.save_user_difficulty()
        return self.get_difficulty_label()

    def adjust_difficulty_after_quiz(self):
        """
        Adjusts difficulty for the *next quiz* based on overall performance.
        - If user got more correct answers, increase difficulty.
        - If user got more incorrect answers, decrease difficulty.
        """
        correct_count, incorrect_count = self.get_user_performance()

        if correct_count > incorrect_count:
            self.user_difficulty = min(2, self.user_difficulty + 1)  # Move towards Hard
        elif incorrect_count > correct_count:
            self.user_difficulty = max(0, self.user_difficulty - 1)  # Move towards Easy

        self.save_user_difficulty()
        return self.get_difficulty_label()

    def get_difficulty_label(self):
        """Maps numerical difficulty level to string labels."""
        difficulty_levels = ["Easy", "Medium", "Hard"]
        return difficulty_levels[self.user_difficulty]


# MCQ Generation Function
def generate_mcqs(user_id, num=10, domain="General Knowledge"):
    """Generates MCQs based on user's adaptive difficulty level."""
    adaptive_learning = AdaptiveLearning(user_id)
    difficulty = adaptive_learning.get_difficulty_label()

    PROMPT = f"""
    You are an expert in {domain}. Generate {num} multiple-choice questions (MCQs) in JSON format.
    Each MCQ should follow this structure:

    [
      {{
        "question": "What does CPU stand for?",
        "A": "Central Processing Unit",
        "B": "Computer Personal Unit",
        "C": "Central Process Unit",
        "D": "Control Processing Unit",
        "answer": "Central Processing Unit",
        "difficulty": "Easy"
      }}
    ]

    Ensure:
    - The questions are relevant to "{domain}".
    - The output is strictly valid JSON.
    - Each question has exactly four options.
    - The correct answer must be one of the options.
    - The difficulty level should be "{difficulty}".
    """

    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": PROMPT}])

    # Extract response text
    mcq_text = response['message']['content']

    # Convert response to JSON
    try:
        mcq_json = json.loads(mcq_text)
        return mcq_json
    except json.JSONDecodeError:
        print("Error: The model response is not valid JSON.")
        return []


# Example Usage
if __name__ == "__main__":
    user_id = 1  # Example user ID
    mcqs = generate_mcqs(user_id)
    print(json.dumps(mcqs, indent=2))
