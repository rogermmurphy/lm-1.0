"""
Configuration for Social & Collaboration Service
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Service
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "social-collaboration")
    SERVICE_PORT: int = int(os.getenv("SERVICE_PORT", "8010"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@lm-postgres:5432/littlemonster")
    
    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

settings = Settings()
