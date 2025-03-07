# API for model integration with web side
from flask import Flask, request, jsonify
from Gemma_2 import generateMCQ, convertToJSON  

app = Flask(__name__)

@app.route('/generate_mcqs', methods=['POST'])
def get_mcqs():
    data = request.json
    domain = data.get('domain')
    num_of_questions = data.get('numOfQuestions', 5)  # Default to 5

    if not domain:
        return jsonify({"error": "Domain is required"}), 400

    # Generate text output from the model
    mcq_text = generateMCQ(domain, num_of_questions)

    # Convert text to JSON using your function
    file_name = "generated_mcqs.json"
    mcq_json = convertToJSON(mcq_text, file_name)

    if mcq_json is None:  # Handle parsing errors
        return jsonify({"error": "Failed to parse model response"}), 500

    return jsonify(mcq_json)  # Return JSON response

if __name__ == '__main__':
    app.run(debug=True)