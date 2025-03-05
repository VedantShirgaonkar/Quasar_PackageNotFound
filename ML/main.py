import json
import os
from scripts.mcq_generator import generate_mcq
from scripts.text_processing import extract_text
from scripts.key_sentence_extraction import extract_key_sentences
from scripts.adaptive_learning import adjust_difficulty

# Ensure Hugging Face tokenizers don't interfere
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def save_mcqs(mcqs, output_file="output/final_mcqs.json"):
    """Saves MCQs in JSON format."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(mcqs, f, indent=4)

if __name__ == "__main__":
    # Accept user input for source file or text
    source = input("Enter PDF file path or paste text: ").strip()
    
    # Extract text from the source
    print("🚀 Extracting text...")
    text = extract_text(source)

    if not text:
        print("❌ No text extracted. Exiting.")
        exit()

    print("\n🔍 Extracted Text Preview:\n", text[:1000])  # Print first 1000 characters for verification
    
    # Extract key sentences for better MCQ generation
    sentences = text.split(". ")
    key_sentences = extract_key_sentences(sentences, top_n=5)  # Adjust `top_n` as needed

    if not key_sentences:
        print("❌ No key sentences extracted. Exiting.")
        exit()

    print(f"✅ Extracted {len(key_sentences)} key sentences.")

    # Generate MCQs using Mistral via Ollama
    mcqs = [generate_mcq(sent) for sent in key_sentences if sent]
    mcqs = [mcq for mcq in mcqs if mcq]  # Remove None values

    # Example user performance data (Simulated for now)
    user_performance = {
        "What is the main purpose of machine learning?": "correct",
        "Which algorithm is best for supervised learning?": "incorrect",
    }

    # Adjust difficulty based on user performance
    updated_mcqs = adjust_difficulty(mcqs, user_performance)

    # Save final structured MCQs
    save_mcqs(updated_mcqs)

    print("✅ Final MCQs saved to output/final_mcqs.json")