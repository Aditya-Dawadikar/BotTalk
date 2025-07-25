def get_all_podcasts(collection):
    return list(collection.find({}, {"_id": 0}))

def add_podcast(collection, podcast):
    result = collection.insert_one(podcast)
    return {"inserted_id": str(result.inserted_id)}