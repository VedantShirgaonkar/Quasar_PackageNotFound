import textstat
import json

def categorize_difficulty(sentence):
    """Determines MCQ difficulty based on text complexity."""
    score = textstat.flesch_reading_ease(sentence)

    if score > 60:
        return "Easy"
    elif 30 <= score <= 60:
        return "Medium"
    else:
        return "Hard"

def adjust_difficulty(mcqs, user_performance):
    """
    Adjusts difficulty levels based on user performance.
    
    user_performance: Dictionary tracking correct/incorrect attempts
                      { "question_text": "correct"/"incorrect" }
    """
    for mcq in mcqs:
        question_text = mcq["question"]
        if question_text in user_performance:
            result = user_performance[question_text]

            if result == "correct" and mcq["difficulty"] != "Hard":
                mcq["difficulty"] = "Medium" if mcq["difficulty"] == "Easy" else "Hard"
            elif result == "incorrect" and mcq["difficulty"] != "Easy":
                mcq["difficulty"] = "Medium" if mcq["difficulty"] == "Hard" else "Easy"

    return mcqs