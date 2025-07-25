import json
import subprocess
import time
from typing import Iterator
import os
from dotenv import load_dotenv
import requests

load_dotenv()

group_id = os.getenv("MINIMAX_GROUP_ID")    #your_group_id
api_key = os.getenv("MINIMAX_API_KEY")    #your_api_key

file_format = 'mp3'  # support mp3/pcm/flac

url = "https://api.minimax.io/v1/t2a_v2?GroupId=" + group_id
headers = {"Content-Type":"application/json", "Authorization":"Bearer " + api_key}


def build_tts_stream_headers() -> dict:
    headers = {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'authorization': "Bearer " + api_key,
    }
    return headers


def build_tts_stream_body(text: str, person:str) -> dict:

    voice_id="male-qn-qingse"
    if person == "guest":
        voice_id="English_Insightful_Speaker"

    body = json.dumps({
        "model":"speech-02-turbo",
        "text":text,
        "stream":True,
        "voice_setting":{
            "voice_id":voice_id,
            "speed":1.0,
            "vol":1.0,
            "pitch":0
        },
        "audio_setting":{
            "sample_rate":32000,
            "bitrate":128000,
            "format":"mp3",
            "channel":1
        }
    })
    return body

# mpv_command = ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"]
# mpv_process = subprocess.Popen(
#     mpv_command,
#     stdin=subprocess.PIPE,
#     stdout=subprocess.DEVNULL,
#     stderr=subprocess.DEVNULL,
# )

def call_tts_stream(text: str, persona:str) -> Iterator[bytes]:
    tts_url = url
    tts_headers = build_tts_stream_headers()
    tts_body = build_tts_stream_body(text, persona)

    response = requests.request("POST", tts_url, stream=True, headers=tts_headers, data=tts_body)
    for chunk in (response.raw):
        if chunk:
            if chunk[:5] == b'data:':
                data = json.loads(chunk[5:])
                if "data" in data and "extra_info" not in data:
                    if "audio" in data["data"]:
                        audio = data["data"]['audio']
                        yield audio


# def audio_play(audio_stream: Iterator[bytes]) -> bytes:
#     audio = b""
#     for chunk in audio_stream:
#         if chunk is not None and chunk != '\n':
#             decoded_hex = bytes.fromhex(chunk)
#             mpv_process.stdin.write(decoded_hex)  # type: ignore
#             mpv_process.stdin.flush()
#             audio += decoded_hex

#     return audio

def audio_collect(audio_stream: Iterator[bytes]) -> bytes:
    """Collect and decode all audio chunks into one binary blob."""
    audio = b""
    for chunk in audio_stream:
        if chunk and chunk != '\n':
            decoded = bytes.fromhex(chunk)
            audio += decoded
    return audio

def minimax_generate_tts(script: dict, output_path="outputs/final.mp3"):
    # Start with an empty file
    open(output_path, 'wb').close()

    for conversation in script.get("conversations", []):
        # Host audio
        host_stream = call_tts_stream(conversation.get("host"), "host")
        host_audio = audio_collect(host_stream)
        with open(output_path, 'ab') as file:
            file.write(host_audio)

        # Guest audio
        guest_stream = call_tts_stream(conversation.get("guest"), "guest")
        guest_audio = audio_collect(guest_stream)
        with open(output_path, 'ab') as file:
            file.write(guest_audio)

    print(f"🎧 Final podcast saved: {output_path}")