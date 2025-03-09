import ollama
import json
from outputFormatter import extract_mcqs

MODEL_NAME = "gemma:2b"


def generateMCQ(domain, numOfQuestions):
    PROMPT = f"""
    You are an expert in {domain}. Generate {numOfQuestions} domain-specific multiple-choice questions (MCQs) in JSON format.
    Each MCQ should follow this exact JSON structure:

    [
      {{
        "question": "What does CPU stand for?",
        "A": "Central Processing Unit",
        "B": "Computer Personal Unit",
        "C": "Central Process Unit",
        "D": "Control Processing Unit",
        "answer": "A"
      }},
      {{
        "question": "Which language is primarily used for web development?",
        "A": "Python",
        "B": "Java",
        "C": "HTML",
        "D": "C++",
        "answer": "C"
      }}
    ]

    Ensure:
    - The questions are relevant to the domain "{domain}".
    - The output is strictly valid JSON.
    - Each question has exactly *four options*.
    - The correct answer must be one of the options.
    - No explanations, only JSON output.
    """

    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": PROMPT}])


    mcq_text = response['message']['content']

    return mcq_text


def convertToJSON(modelTextOutput, fileName):
    try:
        mcq_json = json.loads(modelTextOutput)
        with open(fileName, "w", encoding="utf-8") as f:
            json.dump(mcq_json, f, indent=2)
        return mcq_json
    except json.JSONDecodeError:
        list = extract_mcqs(modelTextOutput)

        with open(fileName, "w", encoding="utf-8") as json_file:
            json.dump(list, json_file, indent=4, ensure_ascii=False)

        return list


def crossCheckAndValidateMCQs(original_mcqs_json, domain):
    
    questions_prompt = json.dumps(original_mcqs_json)
    CROSSCHECK_PROMPT = f"""
    These are the questions and answers attempted by me in JSON format:
    {questions_prompt}

    Please cross-check the questions and options. If any answer is incorrect or needs correction, provide the corrected question, options, and the correct answer. Ensure the output strictly follows this exact JSON structure:

    [
      {{
        "question": "What does CPU stand for?",
        "A": "Central Processing Unit",
        "B": "Computer Personal Unit",
        "C": "Central Process Unit",
        "D": "Control Processing Unit",
        "answer": "A"
      }},
      {{
        "question": "Which language is primarily used for web development?",
        "A": "Python",
        "B": "Java",
        "C": "HTML",
        "D": "C++",
        "answer": "C"
      }}
    ]

    Do not deviate from this format.
"""

  
    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": CROSSCHECK_PROMPT}])

    
    corrected_mcq_text = response['message']['content']

    return corrected_mcq_text


def validateMCQPipeline(domain, numOfQuestions, outputFileName):

    generated_mcqs_text = generateMCQ(domain, numOfQuestions)

    
    generated_mcqs_json = convertToJSON(generated_mcqs_text, outputFileName)

    
    corrected_mcqs_text = crossCheckAndValidateMCQs(generated_mcqs_json, domain)

    corrected_mcqs_json = convertToJSON(corrected_mcqs_text, f"corrected_{outputFileName}")

    return corrected_mcqs_json


# Sample chKER
domain = "Computer Science"
numOfQuestions = 5
outputFileName = "mcqs.json"

corrected_mcqs = validateMCQPipeline(domain, numOfQuestions, outputFileName)
print(corrected_mcqs)