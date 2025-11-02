"""
Text-to-Speech Service - Main Application
Migrated from POC 11 - Uses REAL Azure credentials
"""
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware  # CORS handled by nginx gateway
from lm_common.logging import setup_logging, get_logger
from .config import settings
from .routes import generate

setup_logging(service_name=settings.SERVICE_NAME, level=settings.LOG_LEVEL)
logger = get_logger(__name__)

app = FastAPI(title="Little Monster Text-to-Speech Service", version="1.0.0")
# CORS middleware - DISABLED: CORS is handled by nginx API gateway
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(generate.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.SERVICE_NAME, "version": "1.0.0"}
