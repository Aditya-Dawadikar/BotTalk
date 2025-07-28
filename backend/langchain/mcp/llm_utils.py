from langchain_google_genai import ChatGoogleGenerativeAI
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
