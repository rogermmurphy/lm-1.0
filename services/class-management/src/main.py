"""
Class Management Service - Main Application
FastAPI service for managing classes, assignments, and planner events
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

from .config import settings
from .routes import classes_router, assignments_router

# Create FastAPI app
app = FastAPI(
    title="Class Management Service",
    description="API for managing classes, assignments, and schedules",
    version="1.0.0"
)

# CORS handled by nginx gateway - no need for service-level CORS

# Include routers
app.include_router(classes_router, prefix="/api")
app.include_router(assignments_router, prefix="/api")


# OPTIONS handled by nginx gateway

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
        "service": "Class Management Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "classes": "/api/classes",
            "assignments": "/api/assignments"
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
