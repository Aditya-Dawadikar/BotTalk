from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chat_models import ChatOpenAI
import os
import dotenv
dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_gemini():
    llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-lite",
                google_api_key = GEMINI_API_KEY,
                temperature=0.3
            )
    return llm

# def get_openai():
#     llm = ChatOpenAI(
#         model="gpt-4o-mini",
#         openai_api_key=OPENAI_API_KEY,
#         temperature=0.3
#     )
#     return llm