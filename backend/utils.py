import os
import shutil
import json
from backend.services.s3_service import upload_folder
from backend.services.podcast_service import update_podcast_by_id
from backend.services.job_service import update_job_by_id
import asyncio
from datetime import datetime, timezone

def parse_gemini_planner_output(response_lines: list[str]) -> dict:
    # Join lines into a single string
    joined = "\n".join(response_lines).strip()
    
    # Remove surrounding markdown or stray backticks if they exist
    if joined.startswith("```json"):
        joined = joined.removeprefix("```json").strip()
    if joined.endswith("```"):
        joined = joined.removesuffix("```").strip()
    
    try:
        return json.loads(joined)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

def parse_gemini_json_output(response: str) -> dict:
    # Join lines into a single string
    # Remove surrounding markdown or stray backticks if they exist
    if response.startswith("```json"):
        response = response.removeprefix("```json").strip()
    if response.endswith("```"):
        response = response.removesuffix("```").strip()
    
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

async def upload_and_cleanup_job(job_id: str, podcast_id: str,s3_prefix="jobs"):
    """
    Uploads all files from outputs/<job_id> to S3 and deletes the folder after upload is done.
    """
    folder_path = os.path.join("outputs", job_id)
    if not os.path.exists(folder_path):
        print(f"[ERROR] Folder {folder_path} does not exist.")
        return False

    s3_path_prefix = f"{s3_prefix}/{job_id}"

    utc_now = datetime.now(timezone.utc)
    timestamp_str = utc_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    try:
        # Upload files (runs in a thread to avoid blocking)
        await asyncio.to_thread(upload_folder, folder_path, s3_path_prefix)
        print(f"[INFO] Uploaded all files from {folder_path} to S3 at {s3_path_prefix}")

        # Update Podcast in Mongodb
        update_podcast_by_id(document_id=podcast_id, update_fields={
            "status": "COMPLETE",
            "base_path": s3_path_prefix,
            "audio_file": "final.wav",
            "thumbnail": "thumbnail.png",
            "summary": "summary.json",
            "plan": "planner_output.json",
            "raw_script": "raw_script.txt",
            "final_script": "final_script.txt",
            "job_finished_at": timestamp_str
        })

        update_job_by_id(document_id=job_id, update_fields={
            "end_timestamp": timestamp_str
        })

        # Delete folder (only runs after upload completes)
        await asyncio.to_thread(shutil.rmtree, folder_path)
        print(f"[INFO] Deleted local folder {folder_path}")

        return True
    except Exception as e:
        print(f"[ERROR] Failed during upload or delete for folder {folder_path}: {e}")
        return False
