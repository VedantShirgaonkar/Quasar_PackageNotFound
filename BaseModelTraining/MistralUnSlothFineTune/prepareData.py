# CODE TO PREPARE THE MCQ DATA FOR JSON FORMAT --> for fine tunning of Mistral Model 
import json
import re

def convert_to_jsonl(input_file, output_file, category):
    with open(input_file, "r", encoding="utf-8") as file:
        data = file.read()

    raw_questions = data.strip().split("#Q")[1:]

    processed_data = []
    
    for q in raw_questions:
        lines = q.strip().split("\n")
        
        question = lines[0].strip()  
        correct_answer = lines[1].strip().lstrip("^")  

        options = {}
        correct_option = None

        for line in lines[2:]:
            match = re.match(r"([A-D])\s(.+)", line.strip())  
            if match:
                option, text = match.groups()
                options[option] = text
                if text.strip().lower() == correct_answer.strip().lower():
                    correct_option = option  

        if correct_option:
            processed_data.append({
                "question": question,
                "A": options.get("A", ""),
                "B": options.get("B", ""),
                "C": options.get("C", ""),
                "D": options.get("D", ""),
                "answer": correct_option,
                "category": category  # Add category label
            })

    with open(output_file, "a", encoding="utf-8") as out_file:  # Append to the final dataset
        for entry in processed_data:
            out_file.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Processed {len(processed_data)} questions from {category} and saved to {output_file}")

# Convert multiple category files into one dataset
categories = {
    r"data\fineTunning\science.txt": "Science",
    r"data\fineTunning\generalKnowledge.txt": "General Knowledge",
    r"data\fineTunning\brainteaser.txt": "Brain Teasers",
    r"data\fineTunning\history.txt": "History"
}

final_output = "combined_dataset.jsonl"

# Clear previous dataset
open(final_output, "w").close()

for file, category in categories.items():
    convert_to_jsonl(file, final_output, category)
