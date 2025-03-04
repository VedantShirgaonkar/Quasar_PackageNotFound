from scripts.mcq_generator import generate_mcq
from scripts.key_sentence_extraction import extract_key_sentences
from scripts.text_processing import extract_text
from scripts.output_formatter import format_mcqs_to_json

if __name__ == "__main__":
    input_file = "data/sample.pdf"
    
    sentences = extract_text(input_file)
    key_sentences = extract_key_sentences(sentences, top_n=5)

    mcqs = [generate_mcq(sent) for sent in key_sentences]
    json_output = format_mcqs_to_json(mcqs)

    with open("output/mcq_data.json", "w") as f:
        f.write(json_output)

    print("✅ MCQs generated and saved as JSON!")