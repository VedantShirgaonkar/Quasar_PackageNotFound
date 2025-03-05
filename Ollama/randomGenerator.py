import ollama
import json
import random

# Select the model
MODEL_NAME = "gemma:2b"

# Define multiple domains
domains = ["Computers", "Mathematics", "Science", "History"]
num_questions_per_domain = 3  # Number of MCQs per domain

# List to store all generated questions
all_questions = []

# Loop through each domain and generate MCQs
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

    # Generate MCQs using Ollama
    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": PROMPT}])
    
    # Extract response text
    mcq_text = response['message']['content']

    # Convert response to JSON and store
    try:
        mcq_json = json.loads(mcq_text)  # Parse JSON output
        all_questions.extend(mcq_json)  # Add questions to the list
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON from {domain}. Response:\n", mcq_text)
        

# Shuffle the final list of questions
random.shuffle(all_questions)

# Print the shuffled MCQs
print(json.dumps(all_questions, indent=2))
