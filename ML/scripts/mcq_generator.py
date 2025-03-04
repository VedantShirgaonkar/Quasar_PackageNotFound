import sys
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Ensure the script can access the project directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.key_sentence_extraction import extract_key_sentences
from scripts.text_processing import extract_text
from scripts.output_formatter import format_mcqs_to_json

# Load TinyLlama model & tokenizer (offline mode)
MODEL_PATH = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16, device_map="auto")

def generate_mcq(sentence):
    """
    Generates an MCQ from a given sentence using TinyLlama with a strict format.
    """
    prompt = f"Generate a multiple-choice question based on this sentence:\n'{sentence}'\n\nQuestion:"

    try:
        inputs = tokenizer(prompt, return_tensors="pt").to("mps")  # Optimized for Mac M1/M2
        output = model.generate(**inputs, max_length=150, num_return_sequences=1, do_sample=True, top_p=0.9, temperature=0.7)

        mcq_text = tokenizer.decode(output[0], skip_special_tokens=True)

        print(f"✅ Raw Generated MCQ:\n{mcq_text}\n")  # Debugging print
        return mcq_text

    except Exception as e:
        print(f"❌ Error generating MCQ: {e}")
        return None

# Test MCQ generation
if __name__ == "__main__":
    test_file = "data/sample.pdf"

    print(f"🔍 Checking file existence: {test_file}")
    if not os.path.exists(test_file):
        print("❌ ERROR: File not found!")
    else:
        print("✅ File found. Extracting text...")

    sentences = extract_text(test_file)
    key_sentences = extract_key_sentences(sentences)

    if key_sentences:
        print(f"\n✅ Extracted {len(key_sentences)} key sentences. Starting MCQ generation...\n")
        mcqs = [generate_mcq(sent) for sent in key_sentences]

        # Ensure at least one MCQ is generated
        if any(mcqs):
            json_output = format_mcqs_to_json(mcqs)
            with open("output/mcq_data.json", "w") as f:
                f.write(json_output)

            print("\n✅ MCQs generated and saved as JSON!")
        else:
            print("\n❌ No MCQs were generated. Check for model issues.")

    else:
        print("\n❌ No key sentences found. MCQ generation skipped.")