def get_all_jobs(collection):
    return list(collection.find({}, {"_id": 0}))

def add_job(collection, job):
    result = collection.insert_one(job)
    return {"inserted_id": str(result.inserted_id)}