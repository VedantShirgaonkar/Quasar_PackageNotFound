import sqlite3
from scripts.db_manager import DB_PATH

class AdaptiveLearning:
    def __init__(self, mode="real-time"):
        """
        Initializes adaptive learning mode.
        mode: 
            - "real-time" → Adjusts difficulty after each question
            - "quiz-based" → Adjusts difficulty after an entire quiz
        """
        self.mode = mode  
        self.user_difficulty = 1  # 1 (Medium) → 0 (Easy), 2 (Hard)

    def get_user_performance(self, user_id):
        """Fetches the correct and incorrect answer counts for a user."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM user_performance WHERE user_id = ? AND correct = 1", (user_id,))
        correct_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM user_performance WHERE user_id = ? AND correct = 0", (user_id,))
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

        return self.get_difficulty_label()

    def adjust_difficulty_after_quiz(self, user_id):
        """
        Adjusts difficulty for the *next quiz* based on overall performance.
        - If user got more correct answers, increase difficulty.
        - If user got more incorrect answers, decrease difficulty.
        """
        correct_count, incorrect_count = self.get_user_performance(user_id)

        if correct_count > incorrect_count:
            self.user_difficulty = min(2, self.user_difficulty + 1)  # Move towards Hard
        elif incorrect_count > correct_count:
            self.user_difficulty = max(0, self.user_difficulty - 1)  # Move towards Easy

        return self.get_difficulty_label()

    def get_difficulty_label(self):
        """Maps numerical difficulty level to string labels."""
        difficulty_levels = ["Easy", "Medium", "Hard"]
        return difficulty_levels[self.user_difficulty]