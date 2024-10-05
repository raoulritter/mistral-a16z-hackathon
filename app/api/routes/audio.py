from fastapi import APIRouter, UploadFile, File, HTTPException
from services.whisper_service import WhisperService
from services.mistral_service import MistralService
from core.config import settings

router = APIRouter()

whisper_service = WhisperService()
mistral_service = MistralService(settings.MISTRAL_API_KEY)

@router.post("/process")
async def process_audio(file: UploadFile = File(...)):
    try:
        # Read the audio file
        audio_data = await file.read()
        
        # Transcribe audio
        transcription, timestamps = whisper_service.transcribe(audio_data)
        print(transcription)
        
        # Process transcription with Mistral
        mistral_response = mistral_service.process_transcription(transcription, timestamps)
        print(mistral_response)
        
        return {
            "transcription": transcription,
            "mistral_response": mistral_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def audio_health_check():
    return {"status": "Audio processing is operational"}