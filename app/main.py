from fastapi import FastAPI
from api.routes import audio, image
from core.config import settings
from services.whisper_service import WhisperService
from services.mistral_service import MistralService
from utils.image_processing import encode_image, get_cached_image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup services
whisper_service = WhisperService()
mistral_service = MistralService(settings.MISTRAL_API_KEY)

# Include routers
app.include_router(audio.router, prefix="/audio", tags=["audio"])
app.include_router(image.router, prefix="/image", tags=["image"])

# Paths to your images
reduced_image_path = "data/preload/floorplan_reduced.jpg"
live_image_path = "data/live/live1_r2.jpg"

@app.on_event("startup")
async def startup_event():
    try:
        # Encode images on startup
        for path in [reduced_image_path, live_image_path]:
            base64_image = get_cached_image(path)
            if base64_image is None:
                raise ValueError(f"Failed to encode image: {path}")
    except Exception as e:
        print(f"Error during startup: {str(e)}")
        # You might want to exit the application here if image encoding is critical
        # import sys
        # sys.exit(1)

@app.get("/")
async def root():
    return {"message": "Welcome to the Vision-Impaired Assistance Application"}

# The main processing logic can be moved to a separate endpoint or service method
# For example:
# @app.post("/process")
# async def process_request(request: SomeRequestModel):
#     # Process audio
#     # Analyze images
#     # Generate response using Mistral
#     # Return structured response
#     pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)