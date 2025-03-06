import ollama
import json
from outputFormatter import extract_mcqs

MODEL_NAME = "gemma:2b"  

def generateMCQExplain(domain="Fundamentals Of Operating System",numOfQuestions=10):

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
      "answer": "A",
      "Explaination": "Definition of CPU"
    }},
    {{
      "question": "Which language is primarily used for web development?",
      "A": "Python",
      "B": "Java",
      "C": "HTML",
      "D": "C++",
      "answer": "C",
      "Explaination": "HTML acts as a backbone of Web Development. Ensuring proper structure of the Web-Page"
    }}
  ]

  Ensure:
  - The questions are relevant to the domain "{domain}".
  - The output is strictly valid JSON.
  - Each question has exactly **four options**.
  - The correct answer must be one of the options.
  - Explanation or Hint must be given in brief to justify the correct answers. 
  - only JSON output should be provided.
  """
  # Call the Ollama model
  response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": PROMPT}])

  # Extract the response text
  mcq_text = response['message']['content']

  return mcq_text


def convertToJSON(modelTextOutput,fileName):   
  try:
      mcq_json = json.loads(modelTextOutput)  
      # Printing the JSON output 
      print(json.dumps(mcq_json, indent=2))  
      with open(fileName, "w", encoding="utf-8") as f:
        json.dump(mcq_json, f, indent=2)

  except json.JSONDecodeError:
      print("Error: The model response is not valid JSON.")
      print("Raw response:", modelTextOutput)

      print("Passing the Output Formatter : ")
      list=extract_mcqs(modelTextOutput)

      print(list)
      print("Trying to save the converted json file")

      with open(fileName, "w", encoding="utf-8") as json_file:
        json.dump(list, json_file, indent=4, ensure_ascii=False)


convertToJSON(generateMCQExplain(),"outputCheckExplain.json")





