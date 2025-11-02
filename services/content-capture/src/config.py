"""
Content Capture Service Configuration
"""
import os
from typing import List

class Settings:
    # Service Configuration
    SERVICE_NAME: str = "content-capture"
    SERVICE_PORT: int = int(os.getenv("SERVICE_PORT", "8008"))
    
    # Database Configuration
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "littlemonster")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # JWT Configuration
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key-here")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ]
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    ALLOWED_DOCUMENT_TYPES: List[str] = ["application/pdf", "text/plain"]
    
    # OCR Configuration
    OCR_PROVIDER: str = os.getenv("OCR_PROVIDER", "tesseract")  # tesseract, azure, aws
    AZURE_VISION_KEY: str = os.getenv("AZURE_VISION_KEY", "")
    AZURE_VISION_ENDPOINT: str = os.getenv("AZURE_VISION_ENDPOINT", "")
    
    # Vector Database Configuration
    VECTOR_DB_TYPE: str = os.getenv("VECTOR_DB_TYPE", "chroma")  # chroma, qdrant
    CHROMA_HOST: str = os.getenv("CHROMA_HOST", "localhost")
    CHROMA_PORT: int = int(os.getenv("CHROMA_PORT", "8000"))
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    
    # Embedding Configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))

settings = Settings()
