"""
Route exports for Class Management Service
"""
from .classes import router as classes_router
from .assignments import router as assignments_router

__all__ = ["classes_router", "assignments_router"]
