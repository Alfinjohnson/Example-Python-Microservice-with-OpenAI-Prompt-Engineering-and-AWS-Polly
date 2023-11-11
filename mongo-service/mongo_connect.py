import json
from datetime import datetime
import logging
from pymongo import MongoClient, errors
from const_mongo import MONGO_CONNECT_URL

logging.basicConfig(level=logging.INFO)


def create_template_topic_collection(title, content, settings, references, audio_link, audio_json, status, topic_id,
                                     chapter_name):
    doc = {
        'title': title,  # topic title
        'topic_id': topic_id,
        'chapter_name': chapter_name,
        'content': content,  # topic contents
        'settings': settings,
        'references': references,
        'audio_link': audio_link,
        'audio_json': audio_json,  # audio transcripts
        'created_datetime': datetime.now(),
        'modified_datetime': datetime.now(),
        'status': status
    }
    return doc


def create_topic_settings(pitch, speed, audio_duration):
    settings = {
        'pitch': pitch,
        'speed': speed,
        'audio_duration': audio_duration
    }
    return settings


def create_topic_references(references_no, topic_type, references_link, description):
    references = [{
        'references_no': references_no,
        'type': topic_type,  # video , image
        'link': references_link,
        'description': description  # description for image type
    }]
    return references


def topic_audio_json(start_time, words, topic_id):
    audio_json = [{
        'start_time': start_time,
        'words': words,
        'references_no': topic_id
    }]
    return audio_json


class MongoDBClient:
    def __init__(self, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
        try:
            self.client = MongoClient(MONGO_CONNECT_URL)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
        except errors.ConnectionFailure as e:
            logging.info(f'Error connecting to MongoDB server: {e}')
            exit(1)

    def create_document(self, document):
        try:
            result = self.collection.insert_one(document)
            return result.inserted_id
        except errors.DuplicateKeyError as e:
            logging.info(f'Error inserting document: {e}')

    def read_document(self, topic_id):
        query = {'topic_id': topic_id}
        try:
            result = self.collection.find_one(query)
            logging.info(result)
            return json.loads(json.dumps(result, default=str))  # Convert the result to a JSON-serializable format
        except errors.PyMongoError as e:
            logging.info(f'Error reading document: {e}')

    def update_document(self, topic_id, reference):
        query = {'topic_id': topic_id}
        update = {'$push': {'references': reference}}
        try:
            result = self.collection.update_one(query, update)
            logging.info(result)
            return result
        except errors.PyMongoError as e:
            logging.info(f'Error updating document: {e}')

    def delete_document(self, topic_id):
        query = {'topic_id': topic_id}
        try:
            result = self.collection.delete_one(query)
            return result
        except errors.PyMongoError as e:
            logging.info(f'Error deleting document: {e}')

    def update_recently_viewed_topic(self, topic, chapter):
        chapters_limit = 5
        # Create a document for the recently viewed topic
        recent_topic = {
            'topic': topic,
            'chapters': [],
            'timestamp': datetime.now()
        }
        # Find the document with the specified topic
        query = {'topic': topic}
        existing_topic = self.collection.find_one(query)

        # Update the chapters array if the topic exists
        if existing_topic:
            recent_topic['chapters'] = existing_topic['chapters']
            logging.info(f'Existing topic found: {topic}')

        # Add the new chapter to the chapters array
        recent_topic['chapters'].append(chapter)
        logging.info(f'Added chapter: {chapter} to the topic: {topic}')

        # Trim the chapters array to the specified limit
        recent_topic['chapters'] = recent_topic['chapters'][-chapters_limit:]
        logging.info(f'Trimmed chapters array to {chapters_limit} items')

        # Update the collection with the most recently viewed topic
        self.collection.replace_one(query, recent_topic, upsert=True)
        logging.info(f'Updated collection with the recently viewed topic: {topic}')