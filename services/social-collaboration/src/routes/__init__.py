"""
Routes for Social & Collaboration Service
"""
from fastapi import APIRouter

# Import route modules
from .connections import router as connections_router
from .sharing import router as sharing_router
from .groups import router as groups_router

__all__ = ['connections_router', 'sharing_router', 'groups_router']
