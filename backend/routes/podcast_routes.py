import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from backend.services.podcast_service import get_all_podcasts, get_podcast_by_id
from backend.services.job_service import get_all_jobs, get_job_by_id
from backend.services.s3_service import generate_signed_urls

load_dotenv()

podcast_router = APIRouter()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "bot_talks")
MONGO_PODCAST_COLLECTION = os.getenv("MONGO_PODCAST_COLLECTION", "podcasts")
MONGO_JOBS_COLLECTION = os.getenv("MONGO_JOBS_COLLECTION", "jobs")

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB_NAME]


@podcast_router.get("/podcasts")
def get_podcasts():
    return get_all_podcasts()

@podcast_router.get("/podcast/{podcast_id}")
def fetch_podcast_by_id(podcast_id: str):
    try:
        podcast = get_podcast_by_id(podcast_id)
        if not podcast:
            raise HTTPException(status_code=404, detail="Podcast not found")
        
        if podcast.get("status") != "COMPLETE":
            data = {
                "podcast": podcast,
                "file_urls": {}
            }
        else:
            s3_base_url = podcast.get("base_path")
            urls = generate_signed_urls(s3_base_url)

            file_urls = []
            for key,val in urls.items():
                file_urls.append({
                    "file": key,
                    "url": val
                })

            data = {
                "podcast": podcast,
                "file_urls": file_urls
            }

        return data

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid podcast ID format")

@podcast_router.get("/jobs")
def get_jobs():
    return get_all_jobs()

@podcast_router.get("/job/{job_id}")
def fetch_job_by_id(job_id: str):
    return get_job_by_id(job_id)
