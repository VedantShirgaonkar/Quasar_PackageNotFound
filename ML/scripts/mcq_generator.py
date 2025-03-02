import sys
import os

# Add the project's root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the TinyLlama model & tokenizer (offline mode)
MODEL_PATH = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16, device_map="auto")

def generate_mcq(sentence):
    """
    Generates an MCQ from a given sentence using TinyLlama.
    The output includes a question, 4 answer options, and the correct answer.
    """
    prompt = f"Generate a multiple-choice question based on this sentence:\n'{sentence}'\n\nQuestion:"
    
    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt").to("mps")  # M1 Mac optimization
    
    # Generate response
    output = model.generate(**inputs, max_length=150, num_return_sequences=1)
    
    # Decode output
    mcq_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return mcq_text

# Test MCQ generation
if __name__ == "__main__":
    from scripts.key_sentence_extraction import extract_key_sentences
    from scripts.text_processing import process_input

    # Load key sentences from input PDF/text
    sentences = process_input("data/Hack the Future.pdf")  # Change file as needed
    key_sentences = extract_key_sentences(sentences)

    # Generate MCQs
    print("\n🔹 Generated MCQs:")
    for i, sentence in enumerate(key_sentences, 1):
        mcq = generate_mcq(sentence)
        print(f"\n🔹 MCQ {i}:\n{mcq}")