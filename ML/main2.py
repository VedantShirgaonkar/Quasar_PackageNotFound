import json
import os
import sys
from scripts.mcq_generator import generate_mcq
from scripts.text_processing import extract_text
from scripts.key_sentence_extraction import extract_key_sentences
from scripts.adaptive_learning import AdaptiveLearning

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Backend")))
from database import initialize_database, add_user, get_user_id, store_user_performance, store_mcq

os.environ["TOKENIZERS_PARALLELISM"] = "false"

initialize_database()

def save_mcqs(mcqs, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(mcqs, f, indent=4)

username = input("Enter Your Username: ").strip()
password = input("Enter Your Password: ").strip()

user_id = get_user_id(username, password)
if user_id is None:
    add_user(username, password)
    user_id = get_user_id(username, password)

adaptive_engine = AdaptiveLearning(user_id)

pdf_path = input("Enter PDF File Path: ").strip()
num_questions = int(input("Enter Number of Questions: ").strip())

text = extract_text(pdf_path)
key_sentences = extract_key_sentences(text.split(". "), top_n=num_questions)

mcqs = [generate_mcq(sent, user_id, "Input-Based", adaptive_engine) for sent in key_sentences if sent]
mcqs = [mcq for mcq in mcqs if mcq]

file_path = input("Enter File Path to Store MCQs: ").strip()
save_mcqs(mcqs, file_path)

print(f"✅ MCQs saved to {file_path}")