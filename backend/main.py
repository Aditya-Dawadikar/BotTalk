from fastapi import FastAPI
from agent_router import agent_router

app = FastAPI()

app.include_router(agent_router)