from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import whisper
import requests
import uuid
import os

app = FastAPI()
model = whisper.load_model("tiny.en")  # For low-RAM environments like Render Free

# Existing method — URL-based transcription
class AudioURL(BaseModel):
    url: str

@app.post("/transcribe/url")
def transcribe_from_url(audio: AudioURL):
    temp_filename = f"{uuid.uuid4()}.wav"

    try:
        response = requests.get(audio.url)
        response.raise_for_status()
        
        with open(temp_filename, "wb") as f:
            f.write(response.content)

        result = model.transcribe(temp_filename)
        return {"text": result["text"]}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


# ✅ New method — File upload
@app.post("/transcribe/upload")
async def transcribe_from_upload(file: UploadFile = File(...)):
    temp_filename = f"{uuid.uuid4()}_{file.filename}"

    try:
        # Save uploaded file
        with open(temp_filename, "wb") as f:
            f.write(await file.read())

        result = model.transcribe(temp_filename)
        return {"text": result["text"]}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
