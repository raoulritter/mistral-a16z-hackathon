from fastapi import APIRouter, HTTPException
from utils.image_processing import get_cached_image, reduce_image_size
from core.config import settings

router = APIRouter()

@router.get("/floorplan")
async def get_floorplan():
    floorplan_path = settings.FLOORPLAN_IMAGE_PATH
    base64_image = get_cached_image(floorplan_path)
    if base64_image is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve floorplan image")
    return {"image": base64_image}

@router.get("/live")
async def get_live_image():
    live_image_path = settings.LIVE_IMAGE_PATH
    base64_image = get_cached_image(live_image_path)
    if base64_image is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve live image")
    return {"image": base64_image}

@router.post("/reduce")
async def reduce_image(input_path: str, output_path: str, width: int = 400, height: int = 300, quality: int = 75):
    success = reduce_image_size(input_path, output_path, width, height, quality)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to reduce image size")
    return {"message": "Image successfully reduced"}

@router.get("/health")
async def image_health_check():
    return {"status": "Image processing is operational"}