import os
from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument
from bson import ObjectId
from backend.services.s3_service import generate_signed_urls_batch

load_dotenv()

MONGO_URI = os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "bot_talks")
MONGO_PODCAST_COLLECTION = os.getenv("MONGO_PODCAST_COLLECTION", "podcasts")
MONGO_JOBS_COLLECTION = os.getenv("MONGO_JOBS_COLLECTION", "jobs")

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB_NAME]

PODCAST_COLLECTION = mongo_db[MONGO_PODCAST_COLLECTION]


def convert_id_to_str(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


def get_all_podcasts():
    podcasts = [convert_id_to_str(doc) for doc in PODCAST_COLLECTION.find({})]

    cover_paths = []
    for podcast in podcasts:
        podcast["cover_path"] = f"{podcast.get('base_path')}/{podcast.get('thumbnail')}"
        cover_paths.append(podcast.get("cover_path"))

    signed_urls = generate_signed_urls_batch(cover_paths)

    for podcast in podcasts:
        podcast["cover_url"] = signed_urls[podcast["cover_path"]]

    return podcasts


def add_podcast(podcast):
    result = PODCAST_COLLECTION.insert_one(podcast)
    return {"inserted_id": str(result.inserted_id)}


def get_podcast_by_id(document_id: str):
    try:
        obj_id = ObjectId(document_id)
    except Exception:
        raise ValueError("Invalid document ID format")

    podcast = PODCAST_COLLECTION.find_one({"_id": obj_id})
    return convert_id_to_str(podcast) if podcast else None


def update_podcast_by_id(document_id: str, update_fields: dict):
    try:
        obj_id = ObjectId(document_id)
    except Exception:
        raise ValueError("Invalid document ID format")

    updated_doc = PODCAST_COLLECTION.find_one_and_update(
        {"_id": obj_id},
        {"$set": update_fields},
        return_document=ReturnDocument.AFTER
    )
    return convert_id_to_str(updated_doc) if updated_doc else None
