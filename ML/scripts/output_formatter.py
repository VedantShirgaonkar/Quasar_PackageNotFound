import re
import json

def extract_mcq_components(mcq_text):
    """Extracts structured MCQ components from raw model output."""
    
    # Strict regex to enforce correct MCQ format
    pattern = (
        r'Question:\s*(.+?)\s*\n'  # Capture question
        r'A\)\s*(.+?)\s*\n'  # Capture option A
        r'B\)\s*(.+?)\s*\n'  # Capture option B
        r'C\)\s*(.+?)\s*\n'  # Capture option C
        r'D\)\s*(.+?)\s*\n'  # Capture option D
        r'Answer:\s*([A-D])'  # Capture correct answer
    )

    match = re.search(pattern, mcq_text, re.DOTALL)
    if match:
        question, opt_a, opt_b, opt_c, opt_d, correct_answer = match.groups()
        return {
            "question": question.strip(),
            "options": {
                "A": opt_a.strip(),
                "B": opt_b.strip(),
                "C": opt_c.strip(),
                "D": opt_d.strip()
            },
            "answer": correct_answer.strip()
        }

    return None  # No match means format is incorrect

def format_mcqs_to_json(mcqs):
    """Converts a list of MCQs to JSON format."""
    formatted_mcqs = [extract_mcq_components(mcq) for mcq in mcqs if mcq]
    return json.dumps(formatted_mcqs, indent=4)