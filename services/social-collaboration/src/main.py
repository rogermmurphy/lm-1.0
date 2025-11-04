"""
Social & Collaboration Service - Main Application
FastAPI service for classmate connections, content sharing, and study groups
"""
from fastapi import FastAPI

from .config import settings
from .routes import connections_router, sharing_router, groups_router

# Create FastAPI app with redirect_slashes disabled
app = FastAPI(
    title="Social & Collaboration Service",
    description="API for classmate connections, content sharing, and study groups",
    version="1.0.0",
    redirect_slashes=False
)

# Configure CORS
# CORS handled by nginx gateway

# Include routers
app.include_router(connections_router, prefix="/api")
app.include_router(sharing_router, prefix="/api")
app.include_router(groups_router, prefix="/api")


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
        "service": "Social & Collaboration Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "connections": "/api/connections",
            "sharing": "/api/sharing",
            "groups": "/api/groups"
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
