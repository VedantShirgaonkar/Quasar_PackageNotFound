import textstat
import json

class AdaptiveLearning:
    def __init__(self, mode="real-time"):
        """
        Initializes adaptive learning mode.
        mode: "real-time" (adjusts difficulty after each question) 
              or "quiz-based" (adjusts difficulty after a full quiz)
        """
        self.mode = mode  # Store user-selected mode
        self.user_difficulty = 0.5  # 0 (easy) → 1 (hard)

    def categorize_difficulty(self, sentence):
        """Determines MCQ difficulty based on text complexity (Flesch Reading Score)."""
        score = textstat.flesch_reading_ease(sentence)

        if score > 60:
            return "Easy"
        elif 30 <= score <= 60:
            return "Medium"
        else:
            return "Hard"

    def adjust_difficulty(self, mcqs, user_performance):
        """
        Adjusts difficulty levels based on user performance.

        user_performance: Dictionary tracking correct/incorrect attempts.
                          Format: { "question_text": "correct"/"incorrect" }
        """
        if self.mode == "real-time":
            return self._adjust_difficulty_realtime(mcqs, user_performance)
        else:
            return self._adjust_difficulty_quiz_based(mcqs, user_performance)

    def _adjust_difficulty_realtime(self, mcqs, user_performance):
        """
        Real-Time Mode: Adjusts difficulty of the *next question* based on the last answer.
        """
        updated_mcqs = []
        last_result = None  # Track last question's result

        for mcq in mcqs:
            question_text = mcq["question"]
            if question_text in user_performance:
                last_result = user_performance[question_text]

            if last_result:
                if last_result == "correct":
                    mcq["difficulty"] = "Medium" if mcq["difficulty"] == "Easy" else "Hard"
                elif last_result == "incorrect":
                    mcq["difficulty"] = "Medium" if mcq["difficulty"] == "Hard" else "Easy"

            updated_mcqs.append(mcq)

        return updated_mcqs

    def _adjust_difficulty_quiz_based(self, mcqs, user_performance):
        """
        Quiz-Based Mode: Adjusts difficulty for the *next quiz* based on overall performance.
        """
        correct_count = sum(1 for q in user_performance.values() if q == "correct")
        incorrect_count = len(user_performance) - correct_count

        # Adjust difficulty based on the correct/incorrect ratio
        if correct_count > incorrect_count:  # More correct answers → increase difficulty
            self.user_difficulty = min(1.0, self.user_difficulty + 0.1)
        else:  # More incorrect answers → decrease difficulty
            self.user_difficulty = max(0.1, self.user_difficulty - 0.1)

        # Assign new difficulty to all MCQs
        difficulty_levels = ["Easy", "Medium", "Hard"]
        new_difficulty = difficulty_levels[int(self.user_difficulty * 2)]  # Convert to index

        for mcq in mcqs:
            mcq["difficulty"] = new_difficulty

        return mcqs