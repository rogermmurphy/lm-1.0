"""
Text-to-Speech Service - Configuration
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "text-to-speech-service"
    DEBUG: bool = False
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/littlemonster")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    AZURE_SPEECH_KEY: str = os.getenv("AZURE_SPEECH_KEY", "")
    AZURE_SPEECH_REGION: str = os.getenv("AZURE_SPEECH_REGION", "eastus")
    DEFAULT_VOICE: str = "en-US-JennyNeural"
    AUDIO_DIR: str = os.getenv("AUDIO_DIR", "./data/audio")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
