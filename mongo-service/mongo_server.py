import logging
import re

from const_mongo import MONGO_QA_DATABASE, MONGO_TOPIC_COLLECTION, MONGO_CHAPTER_HISTORY_COLLECTION
from flask import Flask, request, jsonify
from mongo_connect import create_template_topic_collection, MongoDBClient, create_topic_settings

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
topic_client = MongoDBClient(MONGO_QA_DATABASE, MONGO_TOPIC_COLLECTION)
chapter_history_client = MongoDBClient(MONGO_QA_DATABASE, MONGO_CHAPTER_HISTORY_COLLECTION)


@app.route('/test')
def hello_world():
    return 'Endpoint Responded Successfully'


@app.route('/createTopic', methods=['POST'])
def create_topic_collection():
    title = request.json.get("title")
    chapter_name = request.json.get("chapter_name")
    description = request.json.get("description")
    audio_duration = request.json.get("audio_duration")
    audio_link = request.json.get("audio_url")
    word_by_transcript = request.json.get("word_by_transcript")
    logging.info(f"chapter_name: {chapter_name} ,title : {title}, audio_link : {audio_link} ")

    title = title or ""
    chapter_name = chapter_name or ""

    topic_id = re.sub(r'[^a-zA-Z0-9]', '', title) + re.sub(r'[^a-zA-Z0-9]', '', chapter_name)
    logging.info("creating topic collection .. ")
    topic_settings = create_topic_settings(1, 1, audio_duration)
    document = create_template_topic_collection(title, description, topic_settings, [], audio_link, word_by_transcript,
                                                "Active", topic_id, chapter_name)
    create_collection_response = topic_client.create_document(document)
    if not create_collection_response:
        logging.error(
            f"Ran into error while creating topic collection")
        return jsonify({"error": "Ran into error while creating topic collection"}), 500
    logging.info(f"topic collection created object_id: {str(create_collection_response)}")
    return jsonify({"status": 200, "topic_id": topic_id, "doc_id": str(create_collection_response)})


@app.route('/addReference', methods=['PUT'])
def add_reference():
    topic_id = request.json.get("topic_id")
    reference = {
        "ref_topic_id": request.json.get("ref_topic_id"),
        "type": request.json.get("type"),
        "link": request.json.get("link"),
        "description": request.json.get("description"),
        "start_time": request.json.get("start_time")
    }
    logging.info("adding Reference into topic collection .. ")
    adding_reference = topic_client.update_document(topic_id, reference)
    if not adding_reference:
        logging.error(
            f"Ran into error while adding reference to the topic collection")
        return jsonify({"error": "Ran into error while adding reference to the topic collection"}), 500
    logging.info(f"adding reference response: {str(adding_reference)}")
    return jsonify({"status": 200, "response": str(adding_reference)})


@app.route('/getTopic', methods=['GET'])
def get_topic_one():
    topic_id = request.json.get("topic_id")
    logging.info("reading topic collection .. ")
    get_topic_response = topic_client.read_document(topic_id)
    if not get_topic_response:
        logging.error(
            f"Ran into error while reading the topic collection")
        return jsonify({"error": "Ran into error reading the topic collection"}), 500
    logging.info(f"get topic response: {get_topic_response}")
    return get_topic_response


@app.route('/deleteTopic', methods=['POST'])
def delete_topic_one():
    topic_id = request.json.get("topic_id")
    logging.info("delete topic collection .. ")
    delete_topic_response = topic_client.delete_document(topic_id)
    if not delete_topic_response:
        logging.error(
            f"Ran into error while deleting the topic collection {delete_topic_response}")
        return jsonify({"error": "Ran into error deleting the topic collection"}), 500
    logging.info(f"delete topic response: {str(delete_topic_response)}")
    return jsonify({"status": 200, "response": str(delete_topic_response)})


# Chapter history
@app.route('/insertChapterHis', methods=['POST'])
def insert_chapter_his():
    topic = request.json.get("topic")
    chapters = request.json.get("chapters")
    logging.info("Inserting insertChapterHis collection .. ")
    insert_chapter_his_response = chapter_history_client.update_recently_viewed_topic(topic, chapters)
    if not insert_chapter_his_response:
        logging.error(
            f"Ran into error while Inserting insertChapterHis collection")
        return jsonify({"error": "Ran into error while Inserting insertChapterHis collection"}), 500
    logging.info(f"Inserting insertChapterHis collection created object_id: {str(insert_chapter_his_response)}")
    return jsonify({"status": 200})


if __name__ == '__main__':
    app.run(port=8077)
