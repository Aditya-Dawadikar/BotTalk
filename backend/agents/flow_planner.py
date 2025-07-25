from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from mcp.llm_utils import get_gemini

def create_flow_planner_chain():
    prompt = PromptTemplate.from_file("prompts/planner_prompt.txt", input_variables=["topic"])
    llm = get_gemini()
    return LLMChain(llm=llm, prompt=prompt)

def get_checklist(flow_chain, topic):
    output = flow_chain.run(topic)
    return output
