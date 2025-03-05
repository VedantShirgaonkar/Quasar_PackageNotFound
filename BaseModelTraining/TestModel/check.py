from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

def load_model(base_model_id, fine_tuned_repo):
    """Load base model from Hugging Face and apply fine-tuned LoRA adapters."""
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    
    # Load base model from HF
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id, 
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    # Load fine-tuned LoRA weights
    model = PeftModel.from_pretrained(model, fine_tuned_repo)
    
    # Merge LoRA with base model for faster inference
    model = model.merge_and_unload()

    return model, tokenizer

def generate_mcq(model, tokenizer, prompt, max_new_tokens=100):
    """Generate a multiple-choice question in the desired format."""
    
    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    # Generate output
    outputs = model.generate(input_ids=inputs["input_ids"], max_new_tokens=max_new_tokens, use_cache=True)
    
    # Decode and return
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    # Base model from Hugging Face
    base_model_id = "mistralai/Mistral-7B-v0.1"  # Change if using another model

    # Fine-tuned model stored on Hugging Face
    fine_tuned_repo = "uncertainrods/mcq_finetuned_mistral"  # Replace with your repo

    # Load model and tokenizer
    model, tokenizer = load_model(base_model_id, fine_tuned_repo)

    # Define prompt with the required MCQ format
    prompt = """Generate a multiple-choice question on space exploration in the following format:

Question: <your question here>
A) <option A>
B) <option B>
C) <option C>
D) <option D>
Answer: <correct option>"""

    # Generate MCQ
    mcq_output = generate_mcq(model, tokenizer, prompt)
    print("Generated MCQ:\n", mcq_output)
