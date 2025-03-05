from unsloth import FastLanguageModel
import torch
from datasets import load_dataset
from transformers import TrainingArguments
from trl import SFTTrainer

# Configuration
max_seq_length = 2048  # Supports RoPE Scaling internally
dtype = torch.float16  # Optimized for Tesla T4
torch_dtype = torch.float16
load_in_4bit = True  # Memory optimization
model_name = "unsloth/mistral-7b-instruct-v0.3-bnb-4bit"

# Load model and tokenizer
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_name,
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)

# Apply LoRA adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # LoRA rank
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0.1,  # Small dropout to improve generalization
    bias="none",
    use_gradient_checkpointing="unsloth",  # Efficient memory use
    random_state=3407,
)

# Load dataset
train_dataset = load_dataset("json", data_files="mcq_data.jsonl")["train"]  # Update with actual path

# Training setup
training_args = TrainingArguments(
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps=100,
    max_steps=1000,  # Increased steps for better fine-tuning
    learning_rate=1e-4,  # Adjusted for stability
    fp16=True,
    logging_steps=10,
    optim="adamw_8bit",
    weight_decay=0.01,
    lr_scheduler_type="cosine",
    seed=3407,
    output_dir="mcq_finetuned_model",
    save_strategy="steps",
    save_steps=200,
    report_to="none",
)

# Train model
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_dataset,
    dataset_text_field="question",
    max_seq_length=max_seq_length,
    dataset_num_proc=2,
    packing=False,
    args=training_args,
)

trainer.train()

# Save model
trainer.save_model("mcq_finetuned_model")

# Export fine-tuned model
from huggingface_hub import HfApi
api = HfApi()
api.upload_folder(
    folder_path="mcq_finetuned_model",
    repo_id="your_username/mcq_finetuned_mistral",
    repo_type="model"
)

# Enable inference
FastLanguageModel.for_inference(model)

# Sample inference
prompt = "Generate a multiple-choice question on space exploration."
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

outputs = model.generate(input_ids=inputs["input_ids"], max_new_tokens=64, use_cache=True)
print(tokenizer.batch_decode(outputs, skip_special_tokens=True))
