# from chain.podcast_chain import run_podcast_chain
# from tts.gemini_tts import gemini_generate_tts
# from agents.summerizer import create_summerizer
# import json
# from utils import parse_gemini_json_output
# from agents.thumbnail_agent import create_thumbnail_from_description

from nodes.graph import graph

if __name__ == "__main__":
    topic = "How to pray to lord ganesha"
    graph.invoke({"topic":topic})
