import subprocess
import json
from scripts.key_sentence_extraction import extract_key_sentences  # Import extraction function
from scripts.text_processing import extract_text  # Import text extraction
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def generate_mcq(text):
    """Generates an MCQ based on extracted key sentences using Mistral via Ollama (subprocess)."""
    
    sentences = extract_text(text)  # Extract text from PDF
    key_sentences = extract_key_sentences(sentences)  # Extract important sentences

    if not key_sentences:
        print("Error: No key sentences extracted.")
        return None

    prompt = f"""
    Generate a multiple-choice question from the given text.
    Ensure the output is strictly in JSON format with the following keys:
    {{
        "question": "MCQ Question",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "Correct Option"
    }}

    Text: "{' '.join(key_sentences)}"
    """

    # Run Ollama via subprocess
    try:
        response = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        mcq_response = response.stdout.strip()

        # Ensure valid JSON format
        mcq_json = json.loads(mcq_response)
        return mcq_json
    except json.JSONDecodeError:
        print("Error: Model did not return valid JSON.")
        return None
    except subprocess.CalledProcessError as e:
        print("Error running Ollama:", e)
        return None

# Example Usage
if __name__ == "__main__":
    sample_text = "data/sample.pdf"
    mcq = generate_mcq(sample_text)
    if mcq:
        print(json.dumps(mcq, indent=4))