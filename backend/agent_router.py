from fastapi import APIRouter
from agents.tavily_agent import get_tavily_search_results
from nodes.graph import graph
from nodes.graph_node import create_job
import threading
from minimax_tts import minimax_generate_tts
from datetime import datetime, timezone

agent_router = APIRouter()

def run_graph_job(topic: str, job_id: str):
    try:
        graph.invoke({"topic": topic, "job_id": job_id})
    except Exception as e:
        print(f"Error in graph job: {e}")
    finally:
        print(f"Graph job for topic '{topic}' finished.")

@agent_router.get("/agent/podcast")
def trigger_podcast_job(topic:str):

    utc_now = datetime.now(timezone.utc)
    timestamp_str = utc_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    res = create_job(job_data={
        "flow_generated": "no",
        "facts_generated": "no",
        "raw_script_generated": "no",
        "script_generated": "no",
        "audio_generated": "no",
        "summary_generated": "no",
        "image_generated": "no",
        "timestamp": timestamp_str
    })

    # print(res)
    job_id = str(res.get("inserted_id"))

    print(topic, job_id)

    t = threading.Thread(target=run_graph_job, args=(topic,job_id,), daemon=True)
    t.start()

    return {"status": "job received", "topic": topic, "job_id": res.get("inserted_id")}

@agent_router.get("/agent/search")
def tavily_search(query:str):
    input = {
        "query":query,
        "topic":"general",
        "search_depth":"basic",
        "chunks_per_source":3,
        "max_results":10,
        "include_answer":False
    }

    res = get_tavily_search_results(input)
    return 

@agent_router.get("/agent/speak")
def get_minimax_tts():
    script = {
        "conversations": [
            {
                "host": "Hello world",
                "guest": "Hello World"
            }
        ]
    }
    minimax_generate_tts(script, "outputs/final.wav")
    return {"success": True}
