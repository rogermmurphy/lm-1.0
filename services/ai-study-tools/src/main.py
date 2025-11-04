"""
AI Study Tools Service - Main Application
FastAPI service for AI-generated notes, tests, and flashcards
"""
from fastapi import FastAPI

from .config import settings
from .routes import notes_router, tests_router, flashcards_router

# Create FastAPI app
app = FastAPI(
    title="AI Study Tools Service",
    description="API for AI-generated study materials, tests, and flashcards",
    version="1.0.0"
)

# Configure CORS
# CORS handled by nginx gateway

# Include routers
app.include_router(notes_router, prefix="/api")
app.include_router(tests_router, prefix="/api")
app.include_router(flashcards_router, prefix="/api")


# Add OPTIONS handler for CORS preflight
# OPTIONS handled by nginx
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
        "service": "AI Study Tools Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "notes": "/api/notes",
            "tests": "/api/tests",
            "flashcards": "/api/flashcards"
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
