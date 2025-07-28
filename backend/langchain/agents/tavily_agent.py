import os
from dotenv import load_dotenv
from tavily import TavilyClient

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from mcp.llm_utils import get_gemini

load_dotenv()


def create_tavily_agent():
    prompt = PromptTemplate.from_file("prompts/tavily_researcher_prompt.txt", input_variables=["web_search_results"])
    llm = get_gemini()
    return LLMChain(llm=llm, prompt=prompt)


tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def get_tavily_search_results(input:dict):
    response = tavily_client.search(
        query=input.get("query"),
        topic=input.get("topic"),
        search_depth=input.get("search_depth"),
        chunks_per_source=input.get("chunks_per_source"),
        max_results=input.get("max_results"),
        include_answer=input.get("include_answer")   
    )
    return response
