import json
import time
from tts.gemini_tts import gemini_generate_tts
from minimax_tts import minimax_generate_tts
from agents.thumbnail_agent import create_thumbnail_from_description
import traceback
from agents.flow_planner import create_flow_planner_chain, get_checklist
from agents.script_editor import create_script_editor
from agents.host_agent import create_host_agent
from agents.guest_agent import create_guest_agent
from agents.summerizer import create_summerizer
from agents.tavily_agent import create_tavily_agent, get_tavily_search_results
from mcp.context import create_memory
# from podcast_jobs import create_job, update_job


from utils import parse_gemini_planner_output, parse_gemini_json_output

import requests

BASE_URL = "http://localhost:8001"  # Change this to your API server URL


def create_job(job_data: dict):
    """
    Call the /jobs/create API endpoint to create a job.
    
    :param job_data: Dictionary containing job details (e.g., {"title": "My Job", "status": "pending"})
    :return: JSON response from the API
    """
    url = f"{BASE_URL}/jobs"
    response = requests.post(url, json=job_data)

    if response.status_code != 200:
        raise Exception(f"Failed to create job: {response.status_code} - {response.text}")

    return response.json()


def update_job(job_id: str, update_fields: dict):
    """
    Call the /jobs/{job_id} API endpoint to update a job.
    
    :param job_id: Document ID of the job to update
    :param update_fields: Dictionary of fields to update (e.g., {"status": "completed"})
    :return: JSON response from the API
    """
    url = f"{BASE_URL}/jobs"
    payload = {
        "podcast_id": job_id,
        "update_fields": update_fields
    }
    response = requests.put(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"Failed to update job: {response.status_code} - {response.text}")

    return response.json()


memory = create_memory()
flow_chain = create_flow_planner_chain()
host = create_host_agent("prompts/host_prompt.txt", memory)
guest = create_guest_agent("prompts/guest_prompt.txt", memory)
editor = create_script_editor()    
summarizer = create_summerizer()
tavily_agent = create_tavily_agent()

def planner_node(state):
    topic = state["topic"]
    raw_json = get_checklist(flow_chain, topic).split("\n")
    podcast_plan = parse_gemini_planner_output(raw_json)
    with open("outputs/planner_output.json", "w") as f:
        f.write(json.dumps(podcast_plan))
    
    job_id=state["job_id"]
    update_job(job_id, update_fields={
        "flow_generated": "yes"
    })

    print("✅ Podcast Outline Generated")

    return {"planner_output": podcast_plan,
            "script_segments": podcast_plan["segments"],
            "web_search_query": podcast_plan["web_search_query"]}

def host_guest_node(state):
    segments = state["script_segments"]
    tavily_research = state["tavily_research"]

    turns = []

    turns.append({"speaker": "Tavily Research Agent", "text": tavily_research})

    for i, item in enumerate(segments):
        for id, point in enumerate(item.get("key_points",[])):
            seg = f"{id+1}. {point}"

            time.sleep(5)

            print(turns)

            chat_history_str = "\n".join(f"{t['speaker']}: {t['text']}" for t in turns)

            # Host
            host_response = host.invoke({
                "segment": seg,
                "chat_history": chat_history_str
            })
            print(f"\n\n[HOST]: {host_response}")
            turns.append({"speaker": "Host", "text": host_response})

            time.sleep(5)

            chat_history_str = "\n".join(f"{t['speaker']}: {t['text']}" for t in turns)

            # Guest
            guest_response = guest.invoke({
                "segment": seg,
                "chat_history": chat_history_str
            })
            print(f"\n\n[GUEST]: {guest_response}")
            turns.append({"speaker": "Guest", "text": guest_response})

    script = "\n".join(f"{t['speaker']}: {t['text']}" for t in turns)
    with open("outputs/raw_script.txt", "w") as f:
        f.write(json.dumps(script))

    job_id=state["job_id"]
    update_job(job_id, update_fields={
        "raw_script_generated": "yes"
    })

    print("✅ Podcast Dialogues Generated")

    return {"script": script, "turns": turns}

def editor_node(state):
    cleaned = editor.run({"raw_script": state["script"]})
    
    job_id=state["job_id"]
    update_job(job_id, update_fields={
        "script_generated": "yes"
    })

    print("✅ Podcast Script Generated")

    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").strip()
    if cleaned.endswith("```"):
        cleaned = cleaned.removesuffix("```").strip()

    data_dict = json.loads(cleaned)

    with open("outputs/final_script.json", "w") as f:
        f.write(json.dumps(data_dict))

    return {"final_script": data_dict}

def summarizer_node(state):
    content = state["final_script"]
    summary = summarizer.run({"transcript":content})
    parsed_summary = parse_gemini_json_output(summary)
    with open("outputs/summary.json", "w") as f:
        f.write(json.dumps(parsed_summary))

    job_id=state["job_id"]
    update_job(job_id, update_fields={
        "summary_generated": "yes"
    })

    print("✅ Podcast Summary Generated")

    return {"summary": parsed_summary}

def tts_node(state):
    script = state["final_script"]
    # gemini_generate_tts(script, "outputs/final.wav")
    minimax_generate_tts(script, "outputs/final.wav")

    job_id=state["job_id"]
    update_job(job_id, update_fields={
        "audio_generated": "yes"
    })

    print("✅ Podcast Audio Generated")

    return {"audio_generated":True}

def thumbnail_node(state):
    description = state["summary"]["long_desc"]
    create_thumbnail_from_description(description, "outputs/thumbnail.png")

    job_id=state["job_id"]
    update_job(job_id, update_fields={
        "image_generated": "yes"
    })

    print("✅ Podcast Thumbnail Generated")

    return {"thumbnail_generated": True}

def tavily_node(state):
    tavily_query = state["web_search_query"]

    input = {
        "query":tavily_query,
        "topic":"general",
        "search_depth":"basic",
        "chunks_per_source":3,
        "max_results":10,
        "include_answer":True
    }

    res = get_tavily_search_results(input)

    facts_str = res.get("answer","")

    print(facts_str)

    job_id=state["job_id"]
    update_job(job_id, update_fields={
        "facts_generated": "yes"
    })

    print("✅ Tavily Research Done")

    with open("outputs/tavily_research_facts.json", "w") as f:
        f.write(json.dumps(facts_str))

    return {"tavily_research": facts_str}
