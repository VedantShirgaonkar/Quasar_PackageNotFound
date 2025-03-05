import subprocess
import json
import os
from scripts.key_sentence_extraction import extract_key_sentences  # Import extraction function
from scripts.text_processing import extract_text  # Import text extraction

# Suppress Hugging Face tokenizer parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def generate_mcq(text):
    """Generates an MCQ based on extracted key sentences using Mistral via Ollama (subprocess)."""

    # Extract key sentences from the text
    key_sentences = extract_key_sentences(text.split(". "))  # Split text into meaningful parts

    if not key_sentences:
        print("Error: No key sentences extracted.")
        return None

    print("\n📝 Sending to Mistral:\n", key_sentences)

    prompt = f"""
    Generate a multiple-choice question (MCQ) based on the following text:

    "{' '.join(key_sentences)}"

    Ensure the output is strictly in this JSON format:
    {{
        "question": "<Generated MCQ Question>",
        "options": {{
            "A": "<Option A>",
            "B": "<Option B>",
            "C": "<Option C>",
            "D": "<Option D>"
        }},
        "answer": "<Correct Option Letter (A, B, C, or D)>"
    }}
    Only return the JSON object and nothing else.
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

        print("\n🔄 Raw Model Output:\n", mcq_response)

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
    sample_text = "data/sample.pdf"  # Can be a PDF or direct text
    mcq = generate_mcq(sample_text)
    if mcq:
        print(json.dumps(mcq, indent=4))
    else:
        print("MCQ generation failed.")