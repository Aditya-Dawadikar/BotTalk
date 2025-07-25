from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from mcp.llm_utils import get_gemini

def create_summerizer():
    prompt = PromptTemplate.from_file("prompts/summerizer_prompt.txt", input_variables=["transcript"])
    llm = get_gemini()
    return LLMChain(llm=llm, prompt=prompt)