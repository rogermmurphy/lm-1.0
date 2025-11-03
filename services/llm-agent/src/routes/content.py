"""
LLM Agent Service - Content Routes
API endpoints for educational content discovery
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from ..services.content_service import get_content_service

router = APIRouter(prefix="/content", tags=["content"])

# Get content service
content_service = get_content_service()


class ContentSearchRequest(BaseModel):
    """Content search request"""
    query: str
    limit: int = 5


class ContentResponse(BaseModel):
    """Content response"""
    title: str
    summary: str
    url: str
    source: str


@router.post("/search", response_model=List[ContentResponse])
async def search_content(request: ContentSearchRequest):
    """
    Search educational content from multiple sources
    
    - **query**: Search query (topic, concept, question)
    - **limit**: Maximum results to return
    """
    try:
        results = content_service.search_wikipedia(request.query, request.limit)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content search failed: {str(e)}"
        )


@router.get("/wikipedia/{title}")
async def get_wikipedia_article(title: str):
    """
    Get full Wikipedia article
    
    - **title**: Article title
    """
    article = content_service.get_wikipedia_article(title)
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    return article


@router.post("/aggregate")
async def aggregate_content(request: ContentSearchRequest):
    """
    Aggregate content from multiple educational sources
    
    - **query**: Topic to search
    """
    try:
        results = content_service.aggregate_content(request.query)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content aggregation failed: {str(e)}"
        )
