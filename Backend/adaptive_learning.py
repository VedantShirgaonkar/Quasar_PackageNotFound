import sqlite3
import sys
import os

# Add Backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Backend")))

from database import get_db_connection

class AdaptiveLearning:
    """Handles adaptive difficulty adjustments based on user performance."""

    def __init__(self, user_id):
        """
        Initializes difficulty based on the user's stored difficulty level.
        - `user_id`: The ID of the user.
        """
        self.user_id = user_id
        self.user_difficulty = self.get_user_difficulty()

    def get_user_difficulty(self):
        """Fetches the current difficulty level for the user from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT difficulty FROM users WHERE id = ?", (self.user_id,))
        result = cursor.fetchone()

        conn.close()
        return result[0] if result else 1  # Default to Medium (1) if no data

    def update_user_difficulty(self, new_difficulty):
        """Updates the user's difficulty level in the database."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET difficulty = ? WHERE id = ?", (new_difficulty, self.user_id))
        conn.commit()
        conn.close()

        self.user_difficulty = new_difficulty  # Update local variable

    def get_user_performance(self):
        """
        Fetches user performance data:
        - Returns (correct_count, incorrect_count).
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                SUM(CASE WHEN correct = 1 THEN 1 ELSE 0 END),
                SUM(CASE WHEN correct = 0 THEN 1 ELSE 0 END)
            FROM user_performance
            WHERE user_id = ?
        """, (self.user_id,))
        
        correct_count, incorrect_count = cursor.fetchone() or (0, 0)
        conn.close()
        return correct_count, incorrect_count

    def adjust_difficulty_after_quiz(self):
        """
        Adjusts difficulty for the next quiz based on overall performance.
        - If more correct than incorrect, increase difficulty.
        - If more incorrect than correct, decrease difficulty.
        - Saves the updated difficulty in the database.
        """
        correct_count, incorrect_count = self.get_user_performance()

        if correct_count > incorrect_count:
            new_difficulty = min(2, self.user_difficulty + 1)  # Move towards Hard
        elif incorrect_count > correct_count:
            new_difficulty = max(0, self.user_difficulty - 1)  # Move towards Easy
        else:
            new_difficulty = self.user_difficulty  # Keep difficulty the same if tied

        self.update_user_difficulty(new_difficulty)  # Store new difficulty in DB
        return self.get_difficulty_label()

    def get_difficulty_label(self):
        """Returns the current difficulty as a label."""
        return ["Easy", "Medium", "Hard"][self.user_difficulty]