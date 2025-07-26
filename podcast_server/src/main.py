import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Query
from pymongo import MongoClient
from services.podcast_service import get_all_podcasts, add_podcast
from services.job_service import get_all_jobs, add_job, update_job_by_id
from services.s3_service import upload_file, get_presigned_url

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "bot_talks")
MONGO_PODCAST_COLLECTION = os.getenv("MONGO_PODCAST_COLLECTION", "podcasts")
MONGO_JOBS_COLLECTION = os.getenv("MONGO_JOBS_COLLECTION", "jobs")

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB_NAME]

app = FastAPI()

@app.get("/podcasts")
def get_podcasts():
    return get_all_podcasts(mongo_db[MONGO_PODCAST_COLLECTION])

@app.post("/podcasts")
def post_podcast(podcast: dict):
    return add_podcast(mongo_db[MONGO_PODCAST_COLLECTION], podcast)

@app.get("/jobs")
def get_jobs():
    return get_all_jobs(mongo_db[MONGO_JOBS_COLLECTION])

@app.post("/jobs")
def post_job(job: dict):
    return add_job(mongo_db[MONGO_JOBS_COLLECTION], job)

@app.put("/jobs")
def put_job(update_payload:dict):
    return update_job_by_id(mongo_db[MONGO_JOBS_COLLECTION],update_payload.get("podcast_id") ,update_payload.get("update_fields"))

@app.post("/s3_upload")
async def upload_to_s3(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    url = upload_file(file_location, file.filename)
    os.remove(file_location)
    return {"url": url}

@app.get("/s3_file")
def get_s3_file(key: str = Query(..., description="S3 object key (filename)")):
    url = get_presigned_url(key)
    return {"url": url}