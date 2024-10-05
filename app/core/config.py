from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vision-Impaired Assistance Application"
    PROJECT_VERSION: str = "0.1.0"
    MISTRAL_API_KEY: str
    LIVE_IMAGE_PATH: str = "data/live/live1.jpg"
    FLOORPLAN_IMAGE_PATH: str = "data/preload/floorplan.jpg"

    class Config:
        env_file = ".env"

settings = Settings()