"""
Routes for AI Study Tools Service
"""
from fastapi import APIRouter
from .notes import router as notes_router
from .tests import router as tests_router
from .flashcards import router as flashcards_router

__all__ = ['notes_router', 'tests_router', 'flashcards_router']
