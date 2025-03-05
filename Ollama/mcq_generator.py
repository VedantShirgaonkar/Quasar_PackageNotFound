import ollama
import json

# Select the model: 'gemma:2b', 'phi2', or 'tinyllama'
MODEL_NAME = "gemma:2b"  # Change to 'phi2' or 'tinyllama' if needed

num = 10
domain = "Integral Caculus"

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

# Call the Ollama model
response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": PROMPT}])

# Extract the response text
mcq_text = response['message']['content']

# Convert the response to JSON
try:
    mcq_json = json.loads(mcq_text)  # Convert string to JSON
    print(json.dumps(mcq_json, indent=2))  # Pretty-print the JSON
except json.JSONDecodeError:
    print("Error: The model response is not valid JSON.")
    print("Raw response:", mcq_text)
