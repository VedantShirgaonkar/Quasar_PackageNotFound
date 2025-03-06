import json 
import re

def extract_mcqs(text):
    # Improved regex pattern
    pattern = re.compile(
        r'\{\s*"question":\s*"(.*?)",\s*'  # Match question text
        r'"A":\s*"?([^",]+)"?,\s*'  # Match Option A (handle optional quotes)
        r'"B":\s*"?([^",]+)"?,\s*'  # Match Option B
        r'"C":\s*"?([^",]+)"?,\s*'  # Match Option C
        r'"D":\s*"?([^",]+)"?,\s*'  # Match Option D
        r'"answer":\s*"?([ABCD])"?\s*\}'  # Match answer (A/B/C/D only)
    )

    mcqs = []

    for match in pattern.finditer(text):
        mcq = {
            "question": match.group(1).strip(),
            "options": {
                "A": match.group(2).strip(),
                "B": match.group(3).strip(),
                "C": match.group(4).strip(),
                "D": match.group(5).strip()
            },
            "answer": match.group(6).strip()
        }
        mcqs.append(mcq)

    return mcqs

if __name__ == "__main__":
    input_text = '''(Paste your text here)'''
    mcq_list = extract_mcqs(input_text)
    
    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(mcq_list, json_file, indent=4, ensure_ascii=False)
    
    print("MCQs successfully extracted and saved as output.json")