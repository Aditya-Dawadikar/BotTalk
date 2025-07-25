from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from mcp.llm_utils import get_gemini

def create_host_agent(prompt_file, memory):
    prompt = PromptTemplate.from_file(prompt_file, input_variables=["segment", "chat_history"])
    llm = get_gemini()
    return LLMChain(llm=llm, prompt=prompt, memory=memory)
