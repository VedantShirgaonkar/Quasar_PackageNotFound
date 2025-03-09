import sys
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Ensure the script can access the project directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importing all the Script Files for function access
from Backend.text_processing import extract_text
from Backend.output_formatter import format_mcqs_to_json

# Load TinyLlama model & tokenizer (offline mode)
MODEL_PATH = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16, device_map="auto")

def generate_mcqs(text, num_questions=10):
    """
    Generates multiple MCQs from a given text using TinyLlama.
    """
    prompt = f"Generate {num_questions} multiple-choice questions based on this text:\n'{text}'\n\nQuestions:"

    try:
        # MPS --> LOADING OF GPU SHADERS IN CASE OF MACS 
        # CPU / GPU IN CASE OF WINDOWS AS PER AVAILABILITY
        device = "cuda" if torch.cuda.is_available() else "cpu"
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        output = model.generate(**inputs, max_length=150 * num_questions, num_return_sequences=1, do_sample=True, top_p=0.9, temperature=0.7)

        # mcq_text contains the questions which model has generated 
        mcq_text = tokenizer.decode(output[0], skip_special_tokens=True)

        print(f"✅ Raw Generated MCQs:\n{mcq_text}\n")  # Debugging print
        return mcq_text

    except Exception as e:
        print(f"❌ Error generating MCQs: {e}")
        return None

# Test MCQ generation
if __name__ == "__main__":
    test_file = "data/sample.pdf"

    # Testing the PDF path if it Exists or not 
    print(f"🔍 Checking file existence: {test_file}")
    if not os.path.exists(test_file):
        print("❌ ERROR: File not found!")
    else:
        print("✅ File found. Extracting text...")

        # Extract and preprocess text from the PDF
        sentences = extract_text(test_file)
        # preprocessed_text = preprocess_text(sentences)

        # Generate MCQs for the entire preprocessed text
        mcqs = generate_mcqs(sentences, num_questions=10)

        # Ensure MCQs are generated
        if mcqs:
            json_output = format_mcqs_to_json([mcqs])
            with open("output/mcq_data.json", "w") as f:
                f.write(json_output)

            print("\n✅ MCQs generated and saved as JSON!")
        else:
            print("\n❌ No MCQs were generated. Check for model issues.")