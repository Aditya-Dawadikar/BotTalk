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


def convert_id_to_str(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


def get_all_jobs(status: str = "PENDING"):
    cursor = JOBS_COLLECTION.find({"status": status})
    return [convert_id_to_str(doc) for doc in cursor]


def get_job_by_id(document_id: str):
    try:
        obj_id = ObjectId(document_id)
    except Exception:
        raise ValueError("Invalid job ID format")

    job = JOBS_COLLECTION.find_one({"_id": obj_id})
    return convert_id_to_str(job) if job else None


def add_job(job: dict):
    result = JOBS_COLLECTION.insert_one(job)
    return {"inserted_id": str(result.inserted_id)}


def update_job_by_id(document_id: str, update_fields: dict):
    try:
        obj_id = ObjectId(document_id)
    except Exception:
        raise ValueError("Invalid document ID format")

    updated_doc = JOBS_COLLECTION.find_one_and_update(
        {"_id": obj_id},
        {"$set": update_fields},
        return_document=ReturnDocument.AFTER
    )
    return convert_id_to_str(updated_doc) if updated_doc else None
