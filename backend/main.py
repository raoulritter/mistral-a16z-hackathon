from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from utils.audio_processing import process_audio
from utils.image_processing import process_images
from utils.chat_processing import generate_guidance
from utils.whisper_setup import setup_whisper
import os
import sys
import pdb
app = FastAPI()


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))



whisper_pipe = setup_whisper()
print("Whisper setup complete", whisper_pipe)


floorplan_path = os.path.join(project_root, "backend", "data", "preload", "floorplan.jpg")
with open(floorplan_path, "rb") as f:
    floorplan_data = f.read()


# @app.post("/transcribe")
# async def transcribe_endpoint(audio: UploadFile = File(...)):
#     transcription = await process_audio(audio, whisper_pipe)
#     print(transcription)
#     return JSONResponse(content={"transcription": transcription})

@app.post("/transcribe")
async def transcribe_endpoint(audio: UploadFile = File(...)):
    audio_content = await audio.read()
    transcription = process_audio(audio_content, whisper_pipe)
    print(transcription)
    return JSONResponse(content={"transcription": transcription})


# @app.post("/guide")
# async def guide_endpoint(image: UploadFile = File(...), transcription: str = File(...)):
#     print(transcription)
#     image_description = await process_images(image)
#     guidance = await generate_guidance(transcription, image_description)
#     print(guidance)
#     return JSONResponse(content={"guidance": guidance})
# @app.post("/guide")
# async def guide_endpoint(image: UploadFile = File(...), transcription: str = File(...)):
#     # pdb.set_trace()
#     print(transcription)
#     image_content = await image.read()
#     image_description = await process_images(floorplan_data, live_image_data=image_content)
#     guidance = await generate_guidance(transcription, image_description)
#     print(guidance)
#     return JSONResponse(content={"guidance": guidance})

@app.post("/guide")
async def guide_endpoint(image: UploadFile = File(...), transcription: str = File(...)):
    print(transcription)
    image_content = await image.read()
    image_description = process_images(None, image_content)

    
    # Add the processed floorplan to the image description
    # image_description["floorplan"] = processed_floorplan
    
    guidance = await generate_guidance(transcription, image_description)
    print(guidance)
    return JSONResponse(content={"guidance": guidance})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
