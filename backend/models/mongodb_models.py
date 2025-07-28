from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class Podcast(BaseModel):
    title: str
    description: str
    host_name: str
    host_personality: str
    guest_name: str
    guest_personality: str
    timestamp: datetime

class Job(BaseModel):
    flow_generated: Literal["yes", "no", "failed"]
    script_generated: Literal["yes", "no", "failed"]
    audio_generated: Literal["yes", "no", "failed"]
    summary_generated: Literal["yes", "no", "failed"]
    image_generated: Literal["yes", "no", "failed"]
    timestamp: datetime