from scripts.mcq_generator import generate_mcq
from scripts.text_processing import extract_text
from scripts.adaptive_learning import adjust_difficulty
import json

if __name__ == "__main__":
    input_pdf = "data/sample.pdf"

    # Extract structured sentences
    print("🚀 Starting MCQ generation...")
    sentences = extract_text(input_pdf)
    print(f"✅ Extracted {len(sentences)} sentences.")

    # Generate MCQs using Mistral via Ollama
    mcqs = [generate_mcq(input_pdf) for sent in sentences]
    mcqs = [mcq for mcq in mcqs if mcq]  # Remove None values

    # Example user performance data
    user_performance = {
        "What is the main purpose of machine learning?": "correct",
        "Which algorithm is best for supervised learning?": "incorrect",
    }

    # Adjust difficulty based on user performance
    updated_mcqs = adjust_difficulty(mcqs, user_performance)

    # Save final structured MCQs
    with open("output/final_mcqs.json", "w") as f:
        json.dump(updated_mcqs, f, indent=4)

    print("Final MCQs saved to output/final_mcqs.json")