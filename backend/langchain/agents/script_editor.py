from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from backend.langchain.mcp.llm_utils import get_gemini

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # goes to backend/
PROMPT_FILE = os.path.join(BASE_DIR, "langchain", "prompts", "editor_prompt.txt")


def create_script_editor():
    prompt = PromptTemplate.from_file(PROMPT_FILE, input_variables=["raw_script"])
    llm = get_gemini()
    return LLMChain(llm=llm, prompt=prompt)