import subprocess
import json
import os
from scripts.key_sentence_extraction import extract_key_sentences  
from scripts.text_processing import extract_text  
import sys
import os

# Add Backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Backend")))

from database import store_mcq
from scripts.adaptive_learning import AdaptiveLearning

# Suppress Hugging Face tokenizer parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def generate_mcq(text, user_id, domain, difficulty):
    """
    Generates an MCQ using Mistral via Ollama and stores it in the database.
    - `text`: Input text from which the MCQ is generated.
    - `user_id`: ID of the user generating the MCQ.
    - `domain`: "Input-based" or a specific subject category.
    """

   # Initialize adaptive learning to fetch user's current difficulty
    adaptive_engine = AdaptiveLearning(user_id) 
    difficulty = adaptive_engine.get_difficulty_label()

    key_sentences = extract_key_sentences(text.split(". "))  # Extract important sentences
    if not key_sentences:
        return None

    prompt = f"""
    Generate a multiple-choice question (MCQ) based on the following text:

    "{' '.join(key_sentences)}"

    The difficulty level is '{difficulty}', so adjust question complexity accordingly.
    
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

    try:
        response = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        mcq_response = response.stdout.strip()
        mcq_json = json.loads(mcq_response)

        # Assign the current difficulty level to the MCQ before storing
        # mcq_json["difficulty"] = difficulty

        # Store the MCQ in the database
        # store_mcq(user_id, domain, mcq_json)

        return mcq_json
    except json.JSONDecodeError:
        return None
    except subprocess.CalledProcessError:
        return None