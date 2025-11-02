"""
Speech-to-Text Service - Main Application
FastAPI application for audio transcription
Migrated from POC 09 - Production Ready
"""
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware  # CORS handled by nginx gateway
from lm_common.logging import setup_logging, get_logger
from .config import settings
from .routes import transcribe

setup_logging(service_name=settings.SERVICE_NAME, level=settings.LOG_LEVEL)
logger = get_logger(__name__)

app = FastAPI(
    title="Little Monster Speech-to-Text Service",
    description="Audio transcription service using Whisper",
    version="1.0.0"
)

# CORS middleware - DISABLED: CORS is handled by nginx API gateway
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(transcribe.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.SERVICE_NAME, "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
