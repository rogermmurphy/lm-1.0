"""
Gamification Service - Main Application
FastAPI service for points, achievements, and leaderboards
"""
from fastapi import FastAPI

from .config import settings
from .routes import points_router, achievements_router, leaderboards_router

# Create FastAPI app
app = FastAPI(
    title="Gamification Service",
    description="API for points, achievements, and leaderboards",
    version="1.0.0"
)

# Configure CORS
# CORS handled by nginx gateway

# Include routers
app.include_router(points_router, prefix="/api")
app.include_router(achievements_router, prefix="/api")
app.include_router(leaderboards_router, prefix="/api")


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
        "service": "Gamification Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "points": "/api/points",
            "achievements": "/api/achievements",
            "leaderboards": "/api/leaderboards"
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
