"""
Routes for Gamification Service
"""
from .points import router as points_router
from .achievements import router as achievements_router
from .leaderboards import router as leaderboards_router

__all__ = ['points_router', 'achievements_router', 'leaderboards_router']
