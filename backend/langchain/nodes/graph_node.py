import os
import json
import time
from backend.tts.gemini_tts import gemini_generate_tts
from backend.langchain.agents.thumbnail_agent import create_thumbnail_from_description
from backend.langchain.agents.flow_planner import create_flow_planner_chain, get_checklist
from backend.langchain.agents.script_editor import create_script_editor
from backend.langchain.agents.host_agent import create_agent as create_host
from backend.langchain.agents.guest_agent import create_agent as create_guest
from backend.langchain.agents.summerizer import create_summerizer
from backend.langchain.mcp.context import create_memory
from backend.services.job_service import update_job_by_id
from backend.services.podcast_service import update_podcast_by_id

from backend.utils import parse_gemini_planner_output, parse_gemini_json_output

memory = create_memory()
flow_chain = create_flow_planner_chain()
host = create_host("host", "prompts/host_prompt.txt", memory)
guest = create_guest("guest", "prompts/guest_prompt.txt", memory)
editor = create_script_editor()    
summarizer = create_summerizer()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # goes to backend/

def planner_node(state):
    job_id=state["job_id"]
    OUTPUT_FOLDER = state["output_folder"]
    OUTPUT_FOLDER = os.path.join(OUTPUT_FOLDER, job_id)
    topic = state["topic"]

    raw_json = get_checklist(flow_chain, topic).split("\n")
    podcast_plan = parse_gemini_planner_output(raw_json)

    with open(f"{OUTPUT_FOLDER}/planner_output.json", "w") as f:
        f.write(json.dumps(podcast_plan))
    
    update_job_by_id(document_id=job_id, update_fields={
        "flow_generated": "yes"
    })

    print("✅ Podcast Outline Generated")

    return {"planner_output": podcast_plan,
            "script_segments": podcast_plan["segments"]}

def host_guest_node(state):
    job_id=state["job_id"]
    segments = state["script_segments"]
    
    OUTPUT_FOLDER = state["output_folder"]
    OUTPUT_FOLDER = os.path.join(OUTPUT_FOLDER, job_id)
    turns = []

    for i, item in enumerate(segments):
        for id, point in enumerate(item.get("key_points",[])):
            seg = f"{id+1}. {point}"

            time.sleep(5)

            # Host
            host_response = host.run({"segment": seg, "chat_history": turns})
            print(f"\n\n[HOST]: {host_response}")
            turns.append({"speaker": "Host", "text": host_response})

            time.sleep(5)

            # Guest
            guest_response = guest.run({"segment": seg, "chat_history": turns})
            print(f"\n\n[GUEST]: {guest_response}")
            turns.append({"speaker": "Guest", "text": guest_response})

    script = "\n".join(f"{t['speaker']}: {t['text']}" for t in turns)

    with open(f"{OUTPUT_FOLDER}/raw_script.txt", "w") as f:
        f.write(json.dumps(script))

    update_job_by_id(document_id=job_id, update_fields={
        "raw_script_generated": "yes"
    })

    print("✅ Podcast Dialogues Generated")

    return {"script": script, "turns": turns}

def editor_node(state):
    job_id=state["job_id"]
    OUTPUT_FOLDER = state["output_folder"]
    OUTPUT_FOLDER = os.path.join(OUTPUT_FOLDER, job_id)

    cleaned = editor.run({"raw_script": state["script"]})
    
    update_job_by_id(document_id=job_id, update_fields={
        "script_generated": "yes"
    })

    with open(f"{OUTPUT_FOLDER}/final_script.txt", "w") as f:
        f.write(json.dumps(cleaned))

    print("✅ Podcast Script Generated")

    return {"final_script": cleaned}

def summarizer_node(state):
    job_id=state["job_id"]
    podcast_id=state["podcast_id"]
    content = state["final_script"]
    OUTPUT_FOLDER = state["output_folder"]
    OUTPUT_FOLDER = os.path.join(OUTPUT_FOLDER, job_id)

    summary = summarizer.run({"transcript":content})
    parsed_summary = parse_gemini_json_output(summary)

    with open(f"{OUTPUT_FOLDER}/summary.json", "w") as f:
        f.write(json.dumps(parsed_summary))

    update_job_by_id(document_id=job_id, update_fields={
        "summary_generated": "yes"
    })

    update_podcast_by_id(document_id=podcast_id, update_fields={
        "meta_data": parsed_summary
    })

    print("✅ Podcast Summary Generated")

    return {"summary": parsed_summary}

def tts_node(state):
    job_id=state["job_id"]
    script = state["final_script"]
    OUTPUT_FOLDER = state["output_folder"]
    OUTPUT_FOLDER = os.path.join(OUTPUT_FOLDER, job_id)

    gemini_generate_tts(script, f"{OUTPUT_FOLDER}/final.wav")

    update_job_by_id(document_id=job_id, update_fields={
        "audio_generated": "yes"
    })

    print("✅ Podcast Audio Generated")

    return {"audio_generated":True}

def thumbnail_node(state):
    job_id=state["job_id"]
    description = state["summary"]["long_desc"]
    OUTPUT_FOLDER = state["output_folder"]
    OUTPUT_FOLDER = os.path.join(OUTPUT_FOLDER, job_id)

    create_thumbnail_from_description(description, f"{OUTPUT_FOLDER}/thumbnail.png")

    update_job_by_id(document_id=job_id, update_fields={
        "image_generated": "yes"
    })

    print("✅ Podcast Thumbnail Generated")

    return {"thumbnail_generated": True}
