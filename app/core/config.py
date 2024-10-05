from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vision-Impaired Assistance Application"
    PROJECT_VERSION: str = "0.1.0"
    MISTRAL_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()