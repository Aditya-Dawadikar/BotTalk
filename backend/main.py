import os
import threading
from datetime import datetime, timezone
from fastapi import FastAPI
from backend.routes.podcast_routes import podcast_router
from backend.langchain.nodes.graph import graph
from backend.services.job_service import add_job
from backend.services.podcast_service import add_podcast
from backend.utils import upload_and_cleanup_job
import asyncio

OUTPUT_FOLDER = os.path.join(os.getcwd(),"outputs")

app = FastAPI()

app.include_router(podcast_router)

def run_graph_job(topic: str, job_id: str, podcast_id: str,output_folder: str):
    try:
        graph.invoke({"topic": topic, "job_id": job_id, "output_folder": output_folder})
        asyncio.run(upload_and_cleanup_job(job_id=job_id, podcast_id=podcast_id))
    except Exception as e:
        print(f"Error in graph job: {e}")
    finally:
        print(f"Graph job for topic '{topic}' finished.")

@app.post("/agent/podcast")
def trigger_podcast_job(topic:str):

    utc_now = datetime.now(timezone.utc)
    timestamp_str = utc_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    res = add_job(job={
        "flow_generated": "no",
        "raw_script_generated": "no",
        "script_generated": "no",
        "audio_generated": "no",
        "summary_generated": "no",
        "image_generated": "no",
        "start_timestamp": timestamp_str,
        "end_timestamp": None
    })

    job_id = str(res.get("inserted_id"))

    podcast_res = add_podcast({
        "topic": topic,
        "job_id": job_id,
        "status": "PENDING",
        "base_path": f"jobs/{job_id}",
        "audio_file": None,
        "thumbnail": None,
        "summary": None,
        "plan": None,
        "raw_script": None,
        "final_script": None,
        "job_started_at": timestamp_str,
        "job_finished_at": None
    })

    podcast_id = str(podcast_res.get("inserted_id"))

    job_dir = os.path.join(OUTPUT_FOLDER, job_id)
    os.makedirs(job_dir, exist_ok=True)
    print(f"Created directory for job: {job_dir}")

    t = threading.Thread(target=run_graph_job, args=(topic,job_id,podcast_id,OUTPUT_FOLDER), daemon=True)
    t.start()

    return {
                "status": "job received",
                "topic": topic,
                "job_id": res.get("inserted_id"),
                "podcast_id": podcast_res.get("inserted_id")
            }
