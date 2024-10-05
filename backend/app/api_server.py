from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import numpy as np
from whisper_setup import setup_whisper, transcribe_audio
from mistral_api import create_prompt, send_to_mistral

app = FastAPI()

# Initialize Whisper model
whisper_pipe = setup_whisper()

class MistralRequest(BaseModel):
    mistral_api_key: str

@app.post("/process_audio")
async def process_audio(file: UploadFile = File(...), mistral_api_key: str = Form(...)):
    try:
        # Read the audio file
        audio_data = await file.read()
        
        # Transcribe audio
        transcription, timestamps = transcribe_audio(whisper_pipe, audio_data)
        print(transcription, timestamps)
        # Create prompt and send to Mistral API
        prompt = create_prompt(transcription, timestamps)
        mistral_response = send_to_mistral(prompt, mistral_api_key)
        
        return {
            "transcription": transcription,
            "mistral_response": mistral_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))