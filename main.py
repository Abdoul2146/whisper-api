# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import whisper
import requests

app = FastAPI()
model = whisper.load_model("base")

class AudioURL(BaseModel):
    url: str

@app.post("/transcribe")
def transcribe(audio: AudioURL):
    audio_data = requests.get(audio.url)
    with open("temp.wav", "wb") as f:
        f.write(audio_data.content)

    result = model.transcribe("temp.wav")
    return {"text": result["text"]}
