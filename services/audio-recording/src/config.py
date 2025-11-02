"""
Audio Recording Service - Configuration
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "audio-recording-service"
    DEBUG: bool = False
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/littlemonster")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    RECORDINGS_DIR: str = os.getenv("RECORDINGS_DIR", "./data/recordings")
    
    class Config:
        env_file = ".env"

settings = Settings()
