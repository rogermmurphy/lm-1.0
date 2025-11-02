"""
Content Capture Service Routes
"""
from .photos import router as photos_router
from .textbooks import router as textbooks_router

__all__ = ["photos_router", "textbooks_router"]
