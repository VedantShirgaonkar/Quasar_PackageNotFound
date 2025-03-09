import subprocess
import json
import os
from Backend.key_sentence_extraction import extract_key_sentences  
from Backend.text_processing import extract_text  
import sys
import os
# Add Backend directory to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Backend")))
# from adaptive_learning import AdaptiveLearning

# Suppress Hugging Face tokenizer parallelism warning

def generate_mcq(text,difficulty):
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    """
    Generates an MCQ using Mistral via Ollama and stores it in the database.
    - `text`: Input text from which the MCQ is generated.
    - `user_id`: ID of the user generating the MCQ.
    - `domain`: "Input-based" or a specific subject category.
    """

    # Initialize adaptive learning to fetch ,user's current difficulty
    # adaptive_engine = AdaptiveLearning(user_id)
    # difficulty = adaptive_engine.get_difficulty_label()

    key_sentences = extract_key_sentences(text.split(". "))  # Extract important sentences
    if not key_sentences:
        return None

    prompt = f"""
    Generate a multiple-choice question (MCQ) based on the following text:

    "{' '.join(key_sentences)}"

    The difficulty level is '{difficulty}', so adjust question complexity accordingly.
    
[
    {{
      "question": "<Generated MCQ Question>",
      "A": "<Option A>",
      "B": "<Option B>",
      "C": "<Option C>",
      "D": "<Option D>",
      "answer": "A"
    }},
    {{
      "question": "<Generated MCQ Question>",
      "A": "<Option A>",
      "B": "<Option B>",
      "C": "<Option C>",
      "D": "<Option D>",
      "answer": "C"
    }}
  ]

  Ensure:
  - The output is strictly valid JSON.
  - Each question has exactly **four options**.
  - The correct answer must be one of the options.
  - No explanations, only JSON output.
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
        return mcq_json
    except json.JSONDecodeError:
        return None
    except subprocess.CalledProcessError:
        return None