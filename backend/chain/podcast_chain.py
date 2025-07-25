import json
import time
from utils import parse_gemini_planner_output

def run_podcast_chain(topic):
    from mcp.context import create_memory
    from agents.flow_planner import create_flow_planner_chain, get_checklist
    from agents.script_editor import create_script_editor
    from agents.host_agent import create_agent as create_host
    from agents.guest_agent import create_agent as create_guest

    raw_script = []
    memory = create_memory()

    # Create Podcast Outline
    flow_chain = create_flow_planner_chain()
    checklist = get_checklist(flow_chain, topic).split("\n")
    podcast_plan = parse_gemini_planner_output(checklist)
    with open("outputs/planner_output.json", "w") as f:
        f.write(json.dumps(podcast_plan))

    # Generate Dialog
    host = create_host("host", "prompts/host_prompt.txt", memory)
    guest = create_guest("guest", "prompts/guest_prompt.txt", memory)
    for i, item in enumerate(podcast_plan.get("segments",[])):
        for id, point in enumerate(item.get("key_points",[])):
            seg = f"{id+1}. {point}"

            time.sleep(5)

            # Host
            host_response = host.run({"segment": seg, "chat_history": raw_script})
            print(f"\n\n[HOST]: {host_response}")
            raw_script.append(f"Host: {host_response}")

            time.sleep(5)

            # Guest
            guest_response = guest.run({"segment": seg, "chat_history": raw_script})
            print(f"\n\n[GUEST]: {guest_response}")
            raw_script.append(f"Guest: {guest_response}")
    
    # Stitch the responses
    joined_script = "\n".join(raw_script)
    with open("outputs/raw_script.txt", "w") as f:
        f.write(json.dumps(joined_script))

    # Final script editing
    editor = create_script_editor()
    polished = editor.run({"raw_script": joined_script})

    # return final script
    return polished
