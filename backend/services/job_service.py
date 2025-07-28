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

JOBS_COLLECTION = mongo_db[MONGO_JOBS_COLLECTION]

def get_all_jobs():
    return list(JOBS_COLLECTION.find({}, {"_id": 0}))

def get_job_by_id(document_id: str):
    """
    Fetch a job document by its _id.

    Args:
        document_id (str): The string representation of the ObjectId.

    Returns:
        dict or None: The job document with _id as string, or None if not found.
    """
    try:
        obj_id = ObjectId(document_id)
    except Exception:
        raise ValueError("Invalid job ID format")

    job = JOBS_COLLECTION.find_one({"_id": obj_id})
    if not job:
        return None

    job["_id"] = str(job["_id"])
    return dict(job)


def add_job(job:dict):
    result = JOBS_COLLECTION.insert_one(job)
    return {"inserted_id": str(result.inserted_id)}

def update_job_by_id(document_id: str, update_fields: dict):
    """
    Update a job by its _id and return the updated document as a dict.
    """
    try:
        obj_id = ObjectId(document_id)
    except Exception:
        raise ValueError("Invalid document ID format")

    updated_doc = JOBS_COLLECTION.find_one_and_update(
        {"_id": obj_id},
        {"$set": update_fields},
        return_document=ReturnDocument.AFTER
    )
    if not updated_doc:
        return None

    # Convert ObjectId to string for JSON compatibility
    updated_doc["_id"] = str(updated_doc["_id"])
    return dict(updated_doc)