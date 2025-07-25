from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from mcp.llm_utils import get_gemini

def create_script_editor():
    prompt = PromptTemplate.from_file("prompts/editor_prompt.txt", input_variables=["raw_script"])
    llm = get_gemini()
    return LLMChain(llm=llm, prompt=prompt)