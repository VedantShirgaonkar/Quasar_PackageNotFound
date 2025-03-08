import json
import os
from scripts.mcq_generator import generate_mcq
from scripts.text_processing import extract_text
from scripts.key_sentence_extraction import extract_key_sentences
from scripts.adaptive_learning import AdaptiveLearning
import sys
import os

# Add Backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Backend")))

from database import initialize_database, add_user, get_user_id, store_user_performance, store_mcq


# Suppress parallelism warnings from Hugging Face tokenizers
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Ensure database is initialized
initialize_database()

def save_mcqs(mcqs, output_file="output/final_mcqs.json"):
    """Saves MCQs in JSON format to a specified file."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(mcqs, f, indent=4)

if __name__ == "__main__":
    # **User Login / Registration**
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()  

    user_id = get_user_id(username, password)
    if user_id is None:
        print("User not found. Registering new user...")
        add_user(username, password)
        user_id = get_user_id(username, password)

    if user_id is None:
        print("❌ Error: Could not create or retrieve user.")
        exit()

    # **Initialize Adaptive Learning in Quiz-Based Mode**
    adaptive_engine = AdaptiveLearning(user_id)

    # **Extract text from user input (PDF or direct text)**
    source = input("Enter PDF file path or paste text: ").strip()
    text = extract_text(source)

    if not text:
        print("❌ No text extracted. Exiting.")
        exit()

    # **Extract key sentences for MCQ generation**
    key_sentences = extract_key_sentences(text.split(". "), top_n=5)
    if not key_sentences:
        print("❌ No key sentences extracted. Exiting.")
        exit()

    # **Generate MCQs based on extracted sentences**
    mcqs = [generate_mcq(sent, user_id, "Input-Based", adaptive_engine) for sent in key_sentences if sent]
    mcqs = [mcq for mcq in mcqs if mcq]  # Filter out failed generations

    # **User Interaction with MCQs (Storing Performance)**
    for mcq in mcqs:
        print(f"\n{mcq['question']}")
        for option, text in mcq["options"].items():
            print(f"{option}: {text}")

        user_answer = input("Enter your answer (A/B/C/D): ").strip().upper()
        correct = (user_answer == mcq["answer"])

        # Store the user's performance in the database
        question_id = store_mcq(user_id, "Input-Based", mcq)  # Store MCQ and get question ID
        store_user_performance(user_id, question_id, user_answer, correct)  # Pass ID

    # **Adjust difficulty dynamically for the next quiz**
    new_difficulty = adaptive_engine.adjust_difficulty_after_quiz()
    updated_mcqs = [{**mcq, "difficulty": new_difficulty} for mcq in mcqs]

    # **Save MCQs with updated difficulty level**
    save_mcqs(updated_mcqs)

    print(f"\n✅ Quiz completed! Difficulty for next quiz: {new_difficulty}")