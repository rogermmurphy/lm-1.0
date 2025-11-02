"""
Speech-to-Text Service - Configuration
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    SERVICE_NAME: str = "speech-to-text-service"
    DEBUG: bool = False
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/littlemonster")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    WHISPER_MODEL_SIZE: str = os.getenv("WHISPER_MODEL_SIZE", "base")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./data/uploads")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
