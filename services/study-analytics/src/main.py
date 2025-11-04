"""
Study Analytics Service - Main Application
FastAPI service for study session tracking, performance analytics, and goal management
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
from .config import settings
from .routes import sessions, goals

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Study Analytics Service",
    description="Study session tracking, performance analytics, and goal management",
    version="1.0.0"
)

# Configure CORS
# CORS handled by nginx gateway

# Add OPTIONS handler for preflight requests
# OPTIONS handled by nginx
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.service_name,
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Study Analytics Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "sessions": "/api/analytics/sessions",
            "goals": "/api/analytics/goals",
            "health": "/health",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.service_port,
        reload=True
    )
