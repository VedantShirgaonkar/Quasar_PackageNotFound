import re
import json

def extract_mcq_components(mcq_text):
    """
    Extracts structured MCQ components from raw model output.
    
    Expected input format:
    Question: <MCQ Question>
    A) <Option A>
    B) <Option B>
    C) <Option C>
    D) <Option D>
    Answer: <Correct Option (A/B/C/D)>
    
    Returns:
        dict: Structured MCQ if valid, else None.
    """

    # Regex pattern to strictly enforce the expected MCQ format
    pattern = re.compile(
        r'Question:\s*(.+?)\s*\n'  # Capture question
        r'A\)\s*(.+?)\s*\n'        # Capture option A
        r'B\)\s*(.+?)\s*\n'        # Capture option B
        r'C\)\s*(.+?)\s*\n'        # Capture option C
        r'D\)\s*(.+?)\s*\n'        # Capture option D
        r'Answer:\s*([A-D])',      # Capture correct answer
        re.MULTILINE | re.DOTALL   # Ensure multi-line matching
    )

    match = pattern.search(mcq_text)
    
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

    return None  # Return None if format doesn't match