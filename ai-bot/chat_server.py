from flask import Flask, request, jsonify
import logging
from chat_api import chat_def
import flask_cors

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/test')
def hello_world():
    return 'Endpoint Responded Successfully'


@app.route('/askQuestion', methods=['POST'])
def create_topic():
    data = request.get_json()
    question = data.get('question')
    if not question:
        logging.error("question cannot be null or empty")
        return jsonify({"error": "question cannot be null or empty"}), 400
    logging.info(f"question: {question}")
    # sending request to chatGPT
    response = chat_def(question)
    if not response:
        logging.error("response cannot be null or empty")
        return jsonify({"error": "response cannot be null or empty"}), 400
    logging.info(f"response: {response}")
    return jsonify({"response": response, "question": question})


if __name__ == '__main__':
    app.run(port=8088)
