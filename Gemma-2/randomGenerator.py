import ollama
import json
import random
from outputFormatter import extract_mcqs

MODEL_NAME = "gemma:2b"


domains = ["Computers", "Mathematics","Alexander The Great"]
num_questions_per_domain = 3


all_questions = []


for domain in domains:
    PROMPT = f"""
    You are an expert in {domain}. Generate {num_questions_per_domain} domain-specific multiple-choice questions (MCQs) in JSON format.
    Each MCQ should follow this exact structure:

    [
      {{
        "question": "Sample question?",
        "A": "option-1",
        "B": "option-2",
        "C": "option-3",
        "D": "option-4",
        "answer": "Correct Option"
      }}
    ]

    Ensure:
    - Questions are relevant to {domain}.
    - The output is strictly valid JSON.
    - Each question has exactly four options.
    - The correct answer must be one of the options.
    - No explanations, only JSON output.
    """

    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": PROMPT}])
    
   
    mcq_text = response['message']['content']

    
    try:
      # Here we Will First Try to Convert the Question into the JSON format and then append it to the list 
        mcq_json = json.loads(mcq_text)  
        all_questions.extend(mcq_json)  

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON from {domain}. Response:\n", mcq_text)

        print("Passing to Output Formatter...")

        extracted_mcqs = extract_mcqs(mcq_text)  # Extract MCQs

        print(extracted_mcqs)
        print("Trying to save the converted JSON file...🔃")

        mcq_json = json.dumps(extracted_mcqs)  # Convert to JSON string
        mcq_json = json.loads(mcq_json)  # Load back as Python list

        all_questions.extend(mcq_json)

        

random.shuffle(all_questions)

print(json.dumps(all_questions, indent=2))
