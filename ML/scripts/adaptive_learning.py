import sys
import os
import sqlite3

# Ensure the script can access project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

DB_PATH = "storage/mcq_data.db"

class AdaptiveDifficulty:
    def __init__(self, user_id=1):
        """Initialize user difficulty level (default: medium)"""
        self.user_id = user_id
        self.user_level = self.load_user_level()
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Ensure db directory exists

    def load_user_level(self):
        """Loads the last saved difficulty level from the database."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT difficulty FROM user_difficulty WHERE user_id = ?", (self.user_id,))
            row = cursor.fetchone()
            return float(row[0]) if row else 0.5  # Default to medium (0.5) if no record exists

    def save_user_level(self):
        """Saves the updated difficulty level to the database."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_difficulty (user_id, difficulty)
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET difficulty = ?
            ''', (self.user_id, self.user_level, self.user_level))
            conn.commit()

    def update_difficulty(self, correct):
        """
        Adjusts difficulty based on user performance.
        :param correct: Boolean (True = Correct answer, False = Incorrect answer)
        """
        if correct:
            self.user_level += 0.3 * (1 - self.user_level)  # Slightly slower increase
        else:
            self.user_level -= 0.2 * self.user_level  # Faster decrease to reach "easy"  

        # Keep difficulty level within a valid range
        self.user_level = max(0.2, min(0.9, self.user_level))

        # Save updated level
        self.save_user_level()

        return self._get_difficulty()

    def _get_difficulty(self):
        """Returns the difficulty level based on user_level."""
        if self.user_level < 0.4:
            return "easy"
        elif self.user_level < 0.7:
            return "medium"
        else:
            return "hard"

# Test the adaptive difficulty system
if __name__ == "__main__":
    engine = AdaptiveDifficulty()

    print("\n🔹 Initial Difficulty:", engine._get_difficulty())
    print("✔ Correct Answer → New Difficulty:", engine.update_difficulty(True))  # Simulate correct answer
    print("❌ Incorrect Answer → New Difficulty:", engine.update_difficulty(False))  # Simulate wrong answer