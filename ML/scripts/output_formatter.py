import re
import json

def extract_mcq_components(mcq_text):
    """Extracts structured MCQ components from raw model output."""
    print(f"🔍 Parsing MCQ Text:\n{mcq_text}\n")  # Debugging print

    # Improved regex to extract question, options, and answer
    pattern = (
        r'Question:\s*(.+?)\s*\n'
        r'A[\.\)]\s*(.+?)\s*\n'
        r'B[\.\)]\s*(.+?)\s*\n'
        r'C[\.\)]\s*(.+?)\s*\n'
        r'D[\.\)]\s*(.+?)\s*\n'
        r'Answer:\s*([A-D])'
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

    print("❌ Failed to extract MCQ components! Likely incorrect format.")
    return None

def format_mcqs_to_json(mcqs):
    """Converts a list of MCQs to JSON format."""
    formatted_mcqs = [extract_mcq_components(mcq) for mcq in mcqs if mcq]
    return json.dumps(formatted_mcqs, indent=4)