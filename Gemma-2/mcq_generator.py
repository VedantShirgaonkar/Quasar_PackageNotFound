import ollama
import json
from outputFormatter import extract_mcqs

MODEL_NAME = "gemma:2b"  

num = 10
domain = "Donald Trump"

PROMPT = f"""
You are an expert in {domain}. Generate {num} domain-specific multiple-choice questions (MCQs) in JSON format.
Each MCQ should follow this exact JSON structure:

[
  {{
    "question": "What does CPU stand for?",
    "A": "Central Processing Unit",
    "B": "Computer Personal Unit",
    "C": "Central Process Unit",
    "D": "Control Processing Unit",
    "answer": "Central Processing Unit"
  }},
  {{
    "question": "Which language is primarily used for web development?",
    "A": "Python",
    "B": "Java",
    "C": "HTML",
    "D": "C++",
    "answer": "HTML"
  }}
]

Ensure:
- The questions are relevant to the domain "{domain}".
- The output is strictly valid JSON.
- Each question has exactly **four options**.
- The correct answer must be one of the options.
- No explanations, only JSON output.
"""

# Saving the Generate MCQ's
def save_mcqs_to_file(mcqs, filename="mcqs.json"):
    """Save the generated MCQs to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(mcqs, f, indent=2)
    print(f"MCQs saved successfully to {filename}")


# Call the Ollama model
response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": PROMPT}])

# Extract the response text
mcq_text = response['message']['content']

# Convert the response to JSON
try:
    mcq_json = json.loads(mcq_text)  # Convert string to JSON
    # Printing the JSON output 
    print(json.dumps(mcq_json, indent=2))  
    save_mcqs_to_file(mcq_json,"genQuestions/singleDomain.json")

except json.JSONDecodeError:
    # Here We will be using the Reges String Identification to match and convert the answers into JSON 
    # Format whenever the internal json.dump() method fails to convert the text to JSON format
    print("Error: The model response is not valid JSON.")
    print("Raw response:", mcq_text)

    print("Passing the Output Formatter : ")
    list=extract_mcqs(mcq_text)

    print(list)
    print("Trying to save the converted json file")

    with open("genQuestions/raw.json", "w", encoding="utf-8") as json_file:
      json.dump(list, json_file, indent=4, ensure_ascii=False)






