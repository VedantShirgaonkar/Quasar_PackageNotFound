import random

class AdaptiveDifficulty:
    def __init__(self):
        # User difficulty class variable
        self.user_difficulty = 0.5  # Start at medium difficulty

    def update_difficulty(self, correct_responses):
        """Adjusts difficulty based on correct answers."""
        if correct_responses > 3:
            # Updating the Variable each time min/max(1,previous_value+/-1)
            self.user_difficulty = min(1.0, self.user_difficulty + 0.1)
        elif correct_responses < 2:
            self.user_difficulty = max(0.1, self.user_difficulty - 0.1)

    def get_difficulty(self):
        """Returns an adaptive difficulty level for MCQ generation."""
        difficulty_levels = ["easy", "medium", "hard"]
        return random.choices(difficulty_levels, weights=[0.4, 0.4, 0.2])[0]

adaptive_engine = AdaptiveDifficulty()