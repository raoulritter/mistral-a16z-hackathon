from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from utils.image_processing import get_cached_image, reduce_image_size, encode_image
from core.config import settings
from pydantic import BaseModel
from .audio import process_audio
from services.mistral_service import mistral_service
import os

router = APIRouter()

# Global variable to store the floorplan
floorplan_base64 = None


class NavigationRequest(BaseModel):
    task: str
    live_image: UploadFile

@router.on_event("startup")
async def load_floorplan():
    global floorplan_base64
    floorplan_path = settings.FLOORPLAN_IMAGE_PATH
    floorplan_base64 = get_cached_image(floorplan_path)
    if floorplan_base64 is None:
        raise HTTPException(status_code=500, detail="Failed to load floorplan image")

@router.get("/floorplan")
async def get_floorplan():
    global floorplan_base64
    if floorplan_base64 is None:
        raise HTTPException(status_code=500, detail="Floorplan not loaded")
    return {"image": floorplan_base64}


@router.post("/live")
async def process_live_image(file: UploadFile = File(...)):
    contents = await file.read()
    print("Contents: ", contents)
    base64_live_image = encode_image(contents)
    print("Base64 live image: ", base64_live_image)
    if base64_live_image is None:
        raise HTTPException(status_code=500, detail="Failed to process live image")
    return {"image": base64_live_image}

# @router.post("/navigate")
# async def navigate(request: NavigationRequest):
#     print("Navigating")
#     # Get the floorplan and live images
#     floorplan_path = settings.FLOORPLAN_IMAGE_PATH
#     live_image_path = settings.LIVE_IMAGE_PATH
    
#     base64_floorplan = get_cached_image(floorplan_path)
#     base64_live_image = get_cached_image(live_image_path)
    
#     if base64_floorplan is None or base64_live_image is None:
#         raise HTTPException(status_code=500, detail="Failed to retrieve images")
    
#     # Process the audio file
#     audio_result = process_audio(request.audio_file_path)
#     if "error" in audio_result:
#         raise HTTPException(status_code=500, detail=audio_result["error"])
    
#     transcription = audio_result["transcription"]
    
#     # Call Mistral service with images and transcription
#     result = mistral_service.process_task(request.task, base64_floorplan, base64_live_image, transcription)
    
#     return {
#         "navigation": result,
#         "transcription": transcription
#     }

# @router.post("/navigate")
# async def navigate(task: str = Form(...), live_image: UploadFile = File(...)):
#     global floorplan_base64
#     if floorplan_base64 is None:
#         raise HTTPException(status_code=500, detail="Floorplan not loaded")
    
#     contents = await request.live_image.read()
#     base64_live_image = encode_image(contents)
#     if base64_live_image is None:
#         raise HTTPException(status_code=500, detail="Failed to process live image")
    
#     # Process the task with Mistral service
#     result = mistral_service.process_task(request.task, floorplan_base64, base64_live_image)
    
#     return {
#         "navigation": result
#     }

# @router.post("/navigate")
# async def navigate(task: str = Form(...)):
#     global floorplan_base64
#     if floorplan_base64 is None:
#         raise HTTPException(status_code=500, detail="Floorplan not loaded")
    
#     # Hardcode the live image path
#     # live_image_path = "data/live/live1_r2.jpg"
#     live_image_path = "/Users/raoulritter/mistral-a16z-hackathon/app/data/live/live1_r.jpg"
    
#     # Read the hardcoded image
#     with open(live_image_path, "rb") as image_file:
#         contents = image_file.read()
    
#     base64_live_image = encode_image(contents)
#     if base64_live_image is None:
#         raise HTTPException(status_code=500, detail="Failed to process live image")
    
#     # Process the task with Mistral service
#     result = mistral_service.process_task(task, floorplan_base64, base64_live_image)
    
#     return {
#         "navigation": result
#     }
@router.post("/navigate")
async def navigate(task: str = Form(...)):
    global floorplan_base64
    if floorplan_base64 is None:
        raise HTTPException(status_code=500, detail="Floorplan not loaded")
    
    # Process the audio file
    # # audio_result = await process_audio(audio_file)
    # if "error" in audio_result:
    #     raise HTTPException(status_code=500, detail=audio_result["error"])
    
    # transcription = audio_result["transcription"]
    
    # Directory containing the image frames
    transcription = "Help me find the fire exit"
    image_path = '/Users/raoulritter/mistral-a16z-hackathon/IMG_6794_frames'
    
    results = []
    
    # Iterate through all images in the directory
    for filename in sorted(os.listdir(image_path)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # floorplan_path = settings.FLOORPLAN_IMAGE_PATH
            # floorplan_base64 = get_cached_image(floorplan_path)
            file_path = os.path.join(image_path, filename)
            
            # Read the image file
            with open(file_path, "rb") as image_file:
                contents = image_file.read()
            
            base64_live_image = encode_image(contents)
            if base64_live_image is None:
                raise HTTPException(status_code=500, detail=f"Failed to process live image: {filename}")
            
            # Process the task with Mistral service for each frame
            result = mistral_service.process_task(task, floorplan_base64, base64_live_image, transcription)
            results.append({"frame": filename, "navigation": result})
    
    return {
        "frames": results,
        "transcription": transcription
    }

# @router.post("/navigate")
# async def navigate(task: str = Form(...), audio_file: UploadFile = File(...)):
    # global floorplan_base64
    # if floorplan_base64 is None:
    #     raise HTTPException(status_code=500, detail="Floorplan not loaded")
    
    # # Process the audio file
    # audio_data = await audio_file.read()
    # audio_result = await process_audio(audio_file)
    # if "error" in audio_result:
    #     raise HTTPException(status_code=500, detail=audio_result["error"])
    
    # transcription = audio_result["transcription"]
    
    # # Hardcode the live image path
    # live_image_path = "/Users/raoulritter/mistral-a16z-hackathon/app/data/live/live1_r.jpg"
    
    # # Read the hardcoded image
    # with open(live_image_path, "rb") as image_file:
    #     contents = image_file.read()
    
    # base64_live_image = encode_image(contents)
    # if base64_live_image is None:
    #     raise HTTPException(status_code=500, detail="Failed to process live image")
    
    # # Process the task with Mistral service
    # result = mistral_service.process_task(task, floorplan_base64, base64_live_image, transcription)
    
    # return {
    #     "navigation": result,
    #     "transcription": transcription
    # }

@router.post("/reduce")
async def reduce_image(input_path: str, output_path: str, width: int = 400, height: int = 300, quality: int = 75):
    success = reduce_image_size(input_path, output_path, width, height, quality)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to reduce image size")
    return {"message": "Image successfully reduced"}

@router.get("/health")
async def image_health_check():
    return {"status": "Image processing is operational"}