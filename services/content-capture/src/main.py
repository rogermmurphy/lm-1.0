"""
Content Capture Service - Main Application
FastAPI service for photo capture, textbook processing, and vector embeddings
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from config import settings
from routes import photos_router, textbooks_router

# Create FastAPI app
app = FastAPI(
    title="Content Capture Service",
    description="API for photo capture, OCR, textbook processing, and vector embeddings",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(photos_router, prefix="/api")
app.include_router(textbooks_router, prefix="/api")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Content Capture Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "photos": "/api/photos",
            "textbooks": "/api/textbooks"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.SERVICE_PORT,
        reload=True
    )
