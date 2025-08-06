# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import whisper
import requests
import uuid
import os

app = FastAPI()
model = whisper.load_model("tiny.en")  # ✅ Smaller model for Render free tier

class AudioURL(BaseModel):
    url: str

@app.post("/transcribe")
def transcribe(audio: AudioURL):
    # Use unique temp filename to avoid conflicts
    temp_filename = f"{uuid.uuid4()}.wav"

    try:
        # Download audio file
        response = requests.get(audio.url)
        response.raise_for_status()
        
        with open(temp_filename, "wb") as f:
            f.write(response.content)

        # Transcribe
        result = model.transcribe(temp_filename)
        return {"text": result["text"]}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        # Clean up temp file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
