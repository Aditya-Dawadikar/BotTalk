def get_all_jobs(collection):
    return list(collection.find({}, {"_id": 0}))

def add_job(collection, job):
    result = collection.insert_one(job)
    return {"inserted_id": str(result.inserted_id)}

from pymongo import ReturnDocument

from bson import ObjectId
from pymongo import ReturnDocument

def update_job_by_id(collection, document_id: str, update_fields: dict):
    """
    Update a job by its _id and return the updated document as a dict.
    """
    try:
        obj_id = ObjectId(document_id)
    except Exception:
        raise ValueError("Invalid document ID format")

    updated_doc = collection.find_one_and_update(
        {"_id": obj_id},
        {"$set": update_fields},
        return_document=ReturnDocument.AFTER
    )
    if not updated_doc:
        return None

    # Convert ObjectId to string for JSON compatibility
    updated_doc["_id"] = str(updated_doc["_id"])
    return dict(updated_doc)

