from fastapi import FastAPI
from agent_router import agent_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

app.include_router(agent_router)

from fastapi.responses import FileResponse

@app.get("/stream_audio")
def stream_audio(filename: str):
    file_path = f"outputs/{filename}"
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    return FileResponse(file_path, media_type="audio/wav")

from fastapi.responses import FileResponse
import os

@app.get("/podcast_cover")
def get_podcast_cover(filename: str):
    """
    Return the podcast cover image as a file response.
    Example: /podcast_cover?filename=cover.png
    """
    file_path = f"outputs/{filename}"
    if not os.path.exists(file_path):
        return {"error": "Cover image not found"}
    return FileResponse(file_path, media_type="image/png")
