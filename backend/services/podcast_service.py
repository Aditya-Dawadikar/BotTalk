import os
from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument
from bson import ObjectId

load_dotenv()

MONGO_URI = os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "bot_talks")
MONGO_PODCAST_COLLECTION = os.getenv("MONGO_PODCAST_COLLECTION", "podcasts")
MONGO_JOBS_COLLECTION = os.getenv("MONGO_JOBS_COLLECTION", "jobs")

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB_NAME]

PODCAST_COLLECTION = mongo_db[MONGO_PODCAST_COLLECTION]

def get_all_podcasts():
    return list(PODCAST_COLLECTION.find({}, {"_id": 0}))

def add_podcast(podcast):
    result = PODCAST_COLLECTION.insert_one(podcast)
    return {"inserted_id": str(result.inserted_id)}

def get_podcast_by_id(document_id: str):
    """
    Find a podcast document by its _id.

    Args:
        document_id (str): The string representation of the ObjectId.

    Returns:
        dict or None: The podcast document with _id as string, or None if not found.
    """
    try:
        obj_id = ObjectId(document_id)
    except Exception:
        raise ValueError("Invalid document ID format")

    podcast = PODCAST_COLLECTION.find_one({"_id": obj_id})
    if not podcast:
        return None

    podcast["_id"] = str(podcast["_id"])
    return dict(podcast)


def update_podcast_by_id(document_id: str, update_fields: dict):
    """
    Update a job by its _id and return the updated document as a dict.
    """
    try:
        obj_id = ObjectId(document_id)
    except Exception:
        raise ValueError("Invalid document ID format")

    updated_doc = PODCAST_COLLECTION.find_one_and_update(
        {"_id": obj_id},
        {"$set": update_fields},
        return_document=ReturnDocument.AFTER
    )
    if not updated_doc:
        return None

    # Convert ObjectId to string for JSON compatibility
    updated_doc["_id"] = str(updated_doc["_id"])
    return dict(updated_doc)
