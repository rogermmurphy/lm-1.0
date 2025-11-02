"""
LLM Agent Service - Main Application
FastAPI application for AI chat with RAG
Migrated from POC 07 + POC 00 - Production Ready
"""
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware  # CORS handled by nginx gateway

from lm_common.logging import setup_logging, get_logger

from .config import settings
from .routes import chat

# Setup logging
setup_logging(service_name=settings.SERVICE_NAME, level=settings.LOG_LEVEL)
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Little Monster LLM Agent Service",
    description="AI tutoring service with RAG capabilities",
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
app.include_router(chat.router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": "1.0.0",
        "ollama_url": settings.OLLAMA_URL,
        "ollama_model": settings.OLLAMA_MODEL,
        "chromadb": f"{settings.CHROMADB_HOST}:{settings.CHROMADB_PORT}"
    }


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info(f"{settings.SERVICE_NAME} starting up...")
    logger.info(f"LLM Provider: {settings.LLM_PROVIDER}")
    if settings.LLM_PROVIDER.lower() == "bedrock":
        logger.info(f"AWS Bedrock Model: {settings.BEDROCK_MODEL}")
        logger.info(f"AWS Region: {settings.AWS_REGION}")
    else:
        logger.info(f"Ollama: {settings.OLLAMA_URL}")
        logger.info(f"Ollama Model: {settings.OLLAMA_MODEL}")
    logger.info(f"ChromaDB: {settings.CHROMADB_HOST}:{settings.CHROMADB_PORT}")


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
