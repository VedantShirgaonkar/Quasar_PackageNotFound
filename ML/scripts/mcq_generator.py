import sys
import os
import re
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from storage.mcq_database import store_mcq
from scripts.adaptive_learning import AdaptiveDifficulty
from scripts.key_sentence_extraction import extract_key_sentences
from scripts.text_processing import process_input

# Model configuration
MODEL_PATH = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="auto",
    low_cpu_mem_usage=True
)

adaptive_engine = AdaptiveDifficulty()

def extract_mcq_components(mcq_text):
    """Robust MCQ extraction with multiple fallback patterns"""
    # Preprocessing
    mcq_text = re.sub(r'(\n\s*)+', '\n', mcq_text.strip())  # Normalize whitespace
    mcq_text = mcq_text.replace('**', '')  # Remove markdown bold
    
    patterns = [
        # Primary pattern with variations
        r'(?i)Question:\s*(.+?)\n'
        r'A[\.\)]\s*(.+?)\n'
        r'B[\.\)]\s*(.+?)\n'
        r'C[\.\)]\s*(.+?)\n'
        r'D[\.\)]\s*(.+?)\n'
        r'Answer:\s*([A-D])',
        
        # Fallback pattern with different answer notation
        r'(?i)(?:Q|Question)[:\s](.+?)\n'
        r'(A\..+?)\n'
        r'(B\..+?)\n'
        r'(C\..+?)\n'
        r'(D\..+?)\n'
        r'(?:Correct Answer|Answer):?\s*([A-D])'
    ]

    for pattern in patterns:
        match = re.search(pattern, mcq_text, re.DOTALL)
        if match:
            groups = [g.strip() for g in match.groups()]
            question = groups[0]
            options = [re.sub(r'^[A-D][\.\)]\s*', '', g) for g in groups[1:5]]
            correct_answer = groups[5].upper()
            
            # Validate extracted components
            if all(question and options) and correct_answer in {'A','B','C','D'}:
                return question, options, correct_answer
    
    return None, None, None

def generate_mcq(sentence, max_retries=2):
    """Fixed generation with proper prompt separation + EOS token"""
    if not sentence.strip():
        return None, None, None

    prompt = (
        "<<INSTRUCTIONS>>\n"
        "Generate 1 MCQ based ONLY on content below.\n"
        "FORMAT:\n"
        "Question: [Your question]\n"
        "A) [Option A]\nB) [Option B]\nC) [Option C]\nD) [Option D]\n"
        "Answer: [A-D]\n\n"
        "<<EXAMPLES>>\n"
        "Content: HTTP uses port 80\n"
        "Question: Which port does HTTP use?\n"
        "A) 443\nB) 80\nC) 22\nD) 8080\nAnswer: B\n\n"
        "<<CONTENT>>\n"
        f"{sentence}\n\n"
        "<<MCQ TO GENERATE>>\n"
    )

    for attempt in range(max_retries):
        try:
            input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
            outputs = model.generate(
                input_ids,
                max_new_tokens=256,
                temperature=0.8,
                top_p=0.9,
                num_return_sequences=1,
                do_sample=True,
                eos_token_id=tokenizer.eos_token_id  # Use EOS token to stop
            )

            mcq_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            generated_part = mcq_text.split("<<MCQ TO GENERATE>>")[-1].split("<<")[0]
            return extract_mcq_components(generated_part)

        except Exception as e:
            print(f"⚠️ Generation error: {str(e)}")

    return None, None, None



if __name__ == "__main__":
    sentences = process_input("data/Hack the Future.pdf")
    key_sentences = extract_key_sentences(sentences, top_n=5)

    print("\n🔹 Generating MCQs:")
    for idx, sentence in enumerate(key_sentences, 1):
        question, options, correct = generate_mcq(sentence)
        
        if not question:
            print(f"⚠️ Failed to generate MCQ for: '{sentence[:50]}...'")
            continue

        difficulty = adaptive_engine._get_difficulty()
        store_mcq(question, options, correct, difficulty)
        
        print(f"\n✅ MCQ {idx} ({difficulty.upper()}):")
        print(f"Q: {question}")
        for i, opt in enumerate(options, 1):
            print(f"{chr(64+i)}) {opt}")
        print(f"Answer: {correct}\n{'-'*40}")
