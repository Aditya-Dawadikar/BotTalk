from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from backend.langchain.mcp.llm_utils import get_gemini

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # goes to backend/
PROMPT_FILE = os.path.join(BASE_DIR, "langchain", "prompts", "host_prompt.txt")


def create_agent(persona, prompt_file, memory):
    prompt = PromptTemplate.from_file(PROMPT_FILE, input_variables=["segment", "chat_history"])
    llm = get_gemini()
    return LLMChain(llm=llm, prompt=prompt, memory=memory)
