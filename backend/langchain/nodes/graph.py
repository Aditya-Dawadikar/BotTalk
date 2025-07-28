from langgraph.graph import StateGraph, END
from backend.langchain.nodes.graph_node import (planner_node,
                        host_guest_node,
                        editor_node,
                        summarizer_node,
                        thumbnail_node,
                        tts_node)
from langgraph.pregel import RetryPolicy
from typing_extensions import TypedDict
from typing import Any

class State(TypedDict):
    job_id: str
    output_folder: str
    topic: str
    planner_output: Any
    script_segments: Any
    script: Any
    turns: Any
    final_script: Any
    summary: Any
    audio_generate: bool
    thumbnail_node: bool


builder = StateGraph(State)

builder.add_node("planner", planner_node)
builder.add_node("dialogue", host_guest_node)
builder.add_node("editor", editor_node)
builder.add_node("summary", summarizer_node)
builder.add_node("tts", tts_node)
builder.add_node("thumbnail", thumbnail_node, retry_policy=RetryPolicy())

builder.set_entry_point("planner")
builder.add_edge("planner", "dialogue")
builder.add_edge("dialogue", "editor")
builder.add_edge("editor", "summary")
builder.add_edge("editor", "tts")
builder.add_edge("summary", "thumbnail")

builder.add_edge("tts", END)
builder.add_edge("thumbnail", END)

graph = builder.compile()
