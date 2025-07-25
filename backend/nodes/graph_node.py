import json
import time
from tts.gemini_tts import gemini_generate_tts
from agents.thumbnail_agent import create_thumbnail_from_description

from agents.flow_planner import create_flow_planner_chain, get_checklist
from agents.script_editor import create_script_editor
from agents.host_agent import create_agent as create_host
from agents.guest_agent import create_agent as create_guest
from agents.summerizer import create_summerizer
from mcp.context import create_memory

from utils import parse_gemini_planner_output, parse_gemini_json_output

memory = create_memory()
flow_chain = create_flow_planner_chain()
host = create_host("host", "prompts/host_prompt.txt", memory)
guest = create_guest("guest", "prompts/guest_prompt.txt", memory)
editor = create_script_editor()    
summarizer = create_summerizer()

def planner_node(state):
    topic = state["topic"]
    raw_json = get_checklist(flow_chain, topic).split("\n")
    podcast_plan = parse_gemini_planner_output(raw_json)
    with open("outputs/planner_output.json", "w") as f:
        f.write(json.dumps(podcast_plan))
    
    print("✅ Podcast Outline Generated")

    return {"planner_output": podcast_plan,
            "script_segments": podcast_plan["segments"]}

def host_guest_node(state):
    segments = state["script_segments"]
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
    with open("outputs/raw_script.txt", "w") as f:
        f.write(json.dumps(script))

    print("✅ Podcast Dialogues Generated")

    return {"script": script, "turns": turns}

def editor_node(state):
    cleaned = editor.run({"raw_script": state["script"]})
    
    print("✅ Podcast Script Generated")

    return {"final_script": cleaned}

def summarizer_node(state):
    content = state["final_script"]
    summary = summarizer.run({"transcript":content})
    parsed_summary = parse_gemini_json_output(summary)
    with open("outputs/summary.json", "w") as f:
        f.write(json.dumps(parsed_summary))

    print("✅ Podcast Summary Generated")

    return {"summary": parsed_summary}

def tts_node(state):
    script = state["final_script"]
    gemini_generate_tts(script, "outputs/final.wav")

    print("✅ Podcast Audio Generated")

    return {"audio_generated":True}

def thumbnail_node(state):
    description = state["summary"]["long_desc"]
    create_thumbnail_from_description(description, "outputs/thumbnail.png")

    print("✅ Podcast Thumbnail Generated")

    return {"thumbnail_generated": True}
