import json
import logging
import re

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/test')
def hello_world():
    return 'BackEnd Endpoint Responded Successfully'


@app.route('/createTopic', methods=['POST'])
def create_topic_collection():
    title = request.json.get("title")
    description = request.json.get("description")
    chapter_name = request.json.get("chapter_name")
    if not title or not description or not chapter_name:
        logging.info(f"title: {title}, description: {description}, chapter_name: {chapter_name}")
        return jsonify(
            {"status": 400, "title": title, "description": description, "chapter_name": chapter_name})
    logging.info("calling tts service .. ")
    create_tts_request = {"title": title, "description": description}
    headers = {'Content-Type': 'application/json'}
    create_tts_response = requests.post(url="http://127.0.0.1:8066/generateTTS", data=json.dumps(create_tts_request),
                                        headers=headers)
    logging.info(f"create_tts_response: {create_tts_response}")
    logging.info(f"create_tts_response content: {create_tts_response.content}")
    logging.info("calling create topic mongo service .. ")

    tts_response_data = json.loads(create_tts_response.content)
    audio_url = tts_response_data.get("audio_url")
    word_by_transcript = tts_response_data.get("word_by_transcript")
    create_topic_request = {"audio_duration": 0, "title": title, "description": description, "audio_url": audio_url,
                            "word_by_transcript": word_by_transcript, "chapter_name": chapter_name, "title": title}
    create_topic_response = requests.post(url="http://127.0.0.1:8077/createTopic",
                                          data=json.dumps(create_topic_request), headers=headers)
    logging.info(f"create_topic_response: {create_topic_response.content}")
    topic_response_data = json.loads(create_topic_response.content)
    topic_id = topic_response_data.get("topic_id")
    doc_id = topic_response_data.get("doc_id")
    return jsonify(
        {"status": 200, "topic_id": topic_id, "doc_id": doc_id})


@app.route('/addReference', methods=['PUT'])
def add_reference():
    title = request.json.get("title")
    chapter_name = request.json.get("chapter_name")
    start_time = request.json.get("start_time")
    topic_id = request.json.get("topic_id")
    type = request.json.get("type")
    link = request.json.get("link")
    description = request.json.get("description")

    if not title or not chapter_name or not start_time or not type or not link or not description or not topic_id:
        return jsonify({"status": 400, "response": "validate given inputs"})
    ref_topic_id = re.sub(r'[^a-zA-Z0-9]', '', title) + re.sub(r'[^a-zA-Z0-9]', '', chapter_name) + re.sub(
        r'[^a-zA-Z0-9]', '', str(start_time))
    create_topic = {
        "title": ref_topic_id,  # combination of org title +  chapter + start_time
        "chapter_name": chapter_name,
        "description": request.json.get("description")
    }
    headers = {'Content-Type': 'application/json'}
    create_topic_response = requests.post(url="http://127.0.0.1:8044/createTopic", data=json.dumps(create_topic),
                                          headers=headers)
    logging.info(f"create_topic: {create_topic_response}")
    logging.info(f"create_topic content: {create_topic_response.content}")
    logging.info("calling create_topic topic mongo service .. ")

    topic_response_data = json.loads(create_topic_response.content)
    ref_topic_id = topic_response_data.get("topic_id")
    #  ref_doc_id = topic_response_data.get("doc_id")

    add_reference_rq = {
        "ref_topic_id": ref_topic_id,
        "topic_id": topic_id,
        "type": type,
        "link": link,
        "description": description,
        "start_time": start_time
    }
    add_reference_response = requests.put(url="http://127.0.0.1:8077/addReference", data=json.dumps(add_reference_rq),
                                          headers=headers)
    logging.info(f"add_reference_response: {add_reference_response}")
    logging.info(f"add_reference_response content: {add_reference_response.content}")
    logging.info("calling add_reference_response topic mongo service .. ")
    add_reference_response_data = json.loads(add_reference_response.content)

    return jsonify({"status": 200, "ref_topic_id": ref_topic_id})


@app.route('/getB', methods=['GET'])
def get_topic_one():
    return jsonify({"status": 200, "response": str()})


@app.route('/delete', methods=['POST'])
def delete_topic_one():
    return jsonify({"status": 200, "response": str()})


if __name__ == '__main__':
    app.run(port=8044)
