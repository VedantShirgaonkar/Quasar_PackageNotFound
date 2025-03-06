import json
import os
from scripts.mcq_generator import generate_mcq
from scripts.text_processing import extract_text
from scripts.key_sentence_extraction import extract_key_sentences
from scripts.adaptive_learning import AdaptiveLearning
from scripts.db_manager import initialize_database, add_user, get_user_id, store_user_performance

# Ensure Hugging Face tokenizers don't interfere
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Initialize database tables
initialize_database()

def save_mcqs(mcqs, output_file="output/final_mcqs.json"):
    """Saves MCQs in JSON format."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(mcqs, f, indent=4)

if __name__ == "__main__":
    # **User Login / Registration**
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()  # In actual implementation, use hashed passwords

    user_id = get_user_id(username, password)
    if user_id is None:
        print("User not found. Registering new user...")
        add_user(username, password)
        user_id = get_user_id(username, password)

    if user_id is None:
        print("❌ Error: Could not create or retrieve user.")
        exit()

    # **Select Adaptive Learning Mode**
    mode_choice = input("Select Adaptive Learning Mode (1: Real-Time, 2: Quiz-Based): ").strip()
    mode = "real-time" if mode_choice == "1" else "quiz-based"
    adaptive_engine = AdaptiveLearning(mode=mode)

    # **Domain is Hardcoded as "Input-Based" for Your Model**
    domain = "Input-Based"

    # **Extract text from user input (PDF or direct text)**
    source = input("Enter PDF file path or paste text: ").strip()
    text = extract_text(source)

    if not text:
        print("❌ No text extracted. Exiting.")
        exit()

    # **Extract key sentences**
    sentences = text.split(". ")
    key_sentences = extract_key_sentences(sentences, top_n=5)

    if not key_sentences:
        print("❌ No key sentences extracted. Exiting.")
        exit()

    # **Generate MCQs using Mistral**
    mcqs = [generate_mcq(sent, user_id, domain, adaptive_engine) for sent in key_sentences if sent]
    mcqs = [mcq for mcq in mcqs if mcq]

    # **User Interaction with MCQs (Adaptive Learning)**
    user_performance = {}
    for mcq in mcqs:
        print(f"\n{mcq['question']}")
        for option, text in mcq["options"].items():
            print(f"{option}: {text}")

        user_answer = input("Enter your answer (A/B/C/D): ").strip().upper()
        correct = (user_answer == mcq["answer"])

        store_user_performance(user_id, mcq["question"], user_answer, correct)
        user_performance[mcq["question"]] = "correct" if correct else "incorrect"

    # **Adjust difficulty based on chosen mode**
    if mode == "real-time":
        updated_mcqs = [
            {**mcq, "difficulty": adaptive_engine.adjust_difficulty_after_mcq(user_performance[mcq["question"]])}
            for mcq in mcqs
        ]
    else:
        new_difficulty = adaptive_engine.adjust_difficulty_after_quiz(user_id)
        updated_mcqs = [{**mcq, "difficulty": new_difficulty} for mcq in mcqs]

    # **Save MCQs with updated difficulty**
    save_mcqs(updated_mcqs)