from fastapi import APIRouter
from agents.tavily_agent import get_tavily_search_results
from nodes.graph import graph
import threading
from minimax_tts import minimax_generate_tts

agent_router = APIRouter()

def run_graph_job(topic: str):
    try:
        graph.invoke({"topic": topic})
    except Exception as e:
        print(f"Error in graph job: {e}")
    finally:
        print(f"Graph job for topic '{topic}' finished.")

@agent_router.get("/agent/podcast")
def trigger_podcast_job(topic:str):
    t = threading.Thread(target=run_graph_job, args=(topic,), daemon=True)
    t.start()

    return {"status": "job received", "topic": topic}

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
