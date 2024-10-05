import io
import os
from dotenv import load_dotenv
from utils.whisper_setup import setup_whisper, transcribe_audio as whisper_transcribe

# Load environment variables
load_dotenv()

# Initialize Whisper model
whisper_pipe = setup_whisper()

# async def transcribe_audio(audio_file):
#     audio_data = await audio_file.read()
#     transcription, timestamps = whisper_transcribe(whisper_pipe, audio_data)
#     return transcription


async def process_audio(audio_file):
    audio_data = await audio_file.read()
    transcription, timestamps = whisper_transcribe(whisper_pipe, audio_data)
    return transcription

# You can keep the process_audio function here if needed
def process_audio(audio_data, whisper_pipe):
    transcription, timestamps = whisper_transcribe(whisper_pipe, audio_data)
    return {"transcription": transcription, "timestamps": timestamps}