"""
Authentication Service - Main Application
FastAPI application for user authentication
Migrated from POC 12 - Production Ready
"""
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware  # CORS handled by nginx gateway

from lm_common.logging import setup_logging, get_logger

from .config import settings
from .routes import auth

# Setup logging
setup_logging(service_name=settings.SERVICE_NAME, level=settings.LOG_LEVEL)
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Little Monster Authentication Service",
    description="User authentication and authorization service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - DISABLED: CORS is handled by nginx API gateway
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Include routers
app.include_router(auth.router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": "1.0.0"
    }


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info(f"{settings.SERVICE_NAME} starting up...")
    logger.info(f"Debug mode: {settings.DEBUG}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info(f"{settings.SERVICE_NAME} shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
