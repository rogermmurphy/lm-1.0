"""
Logging Utilities
Structured logging configuration for microservices
"""
import logging
import sys
from typing import Optional
import os


# Default log level from environment
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Service name from environment
SERVICE_NAME = os.getenv("SERVICE_NAME", "unknown")


def setup_logging(
    service_name: Optional[str] = None,
    level: Optional[str] = None,
    format_json: bool = False
) -> None:
    """
    Setup logging configuration for the service
    
    Args:
        service_name: Name of the service
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_json: Whether to output logs in JSON format
    """
    service = service_name or SERVICE_NAME
    log_level = level or LOG_LEVEL
    
    # Create formatter
    if format_json:
        # JSON format for production
        log_format = (
            '{"time":"%(asctime)s", '
            '"service":"' + service + '", '
            '"level":"%(levelname)s", '
            '"name":"%(name)s", '
            '"message":"%(message)s"}'
        )
    else:
        # Human-readable format for development
        log_format = (
            f"%(asctime)s - {service} - %(name)s - %(levelname)s - %(message)s"
        )
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set level for specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
