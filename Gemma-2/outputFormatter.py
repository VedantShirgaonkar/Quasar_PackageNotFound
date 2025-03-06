import json 
import re


def extract_mcqs(text):
    # Find potential JSON objects using regex (loosely match MCQ structures)
    matches = re.findall(r'\{.*?\}', text, re.DOTALL)

    mcqs = []
    
    for match in matches:
        try:
            mcq_data = json.loads(match)  # Parse JSON
            mcqs.append({
                "question": mcq_data["question"],
                "options": {
                    "A": mcq_data["A"],
                    "B": mcq_data["B"],
                    "C": mcq_data["C"],
                    "D": mcq_data["D"]
                },
                "answer": mcq_data["answer"]
            })
        except (json.JSONDecodeError, KeyError):
            continue  # Skip invalid JSON blocks

    return mcqs



def extract_mcqs_explnation():
    pass

if __name__ == "__main__":
    input_text = '''(Paste your text here)'''
    mcq_list = extract_mcqs(input_text)
    
    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(mcq_list, json_file, indent=4, ensure_ascii=False)
    
    print("MCQs successfully extracted and saved as output.json")