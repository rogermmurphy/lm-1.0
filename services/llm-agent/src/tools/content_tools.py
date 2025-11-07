"""
Content Capture Tools
LangChain tools for interacting with content-capture-service (photos & textbooks)
"""
from langchain_core.tools import tool
import httpx
import os
from typing import Optional

# Service URL from environment or default to Docker service name
CONTENT_SERVICE_URL = os.getenv("CONTENT_SERVICE_URL", "http://content-capture-service:8008")

# Note: This service requires JWT authentication which tools don't currently have access to.
# Tools will return auth errors until backend integration is improved.
# The tool implementation is structurally correct for when auth is properly handled.


@tool
def list_my_photos(class_id: Optional[int] = None, limit: int = 10) -> str:
    """List user's uploaded photos with OCR extracted text.
    
    Use this tool when the user wants to see their uploaded photos or review OCR results.
    Photos can be filtered by class and results are paginated.
    
    Args:
        class_id: Optional class ID to filter photos (default: None = all classes)
        limit: Maximum number of photos to return (default: 10, max: 50)
    
    Returns:
        String with formatted list of photos including titles and OCR text, or error message.
    """
    try:
        params = {"limit": min(limit, 50)}
        if class_id:
            params["class_id"] = class_id
        
        response = httpx.get(
            f"{CONTENT_SERVICE_URL}/api/photos",
            params=params,
            timeout=10.0
        )
        
        if response.status_code == 200:
            data = response.json()
            photos = data.get("photos", [])
            total = data.get("total", 0)
            
            if not photos:
                return "No photos found. Upload photos through the app to see them here."
            
            result = f"✓ Found {len(photos)} photo(s) (Total: {total})\n\n"
            
            for photo in photos:
                result += f"📷 Photo ID: {photo['id']}\n"
                result += f"  Title: {photo['title']}\n"
                if photo.get('class_id'):
                    result += f"  Class ID: {photo['class_id']}\n"
                result += f"  Status: {photo['extraction_status']}\n"
                
                if photo.get('extracted_text'):
                    text_preview = photo['extracted_text'][:200]
                    if len(photo['extracted_text']) > 200:
                        text_preview += "..."
                    result += f"  OCR Text: {text_preview}\n"
                else:
                    result += "  OCR Text: (none extracted)\n"
                    
                result += f"  Uploaded: {photo.get('created_at', 'unknown')}\n\n"
            
            return result
            
        elif response.status_code == 401:
            return "Authentication required. This feature requires user authentication which is not yet integrated with agent tools."
        elif response.status_code == 404:
            return "Photo service endpoint not found. The service may not be running."
        else:
            return f"Error retrieving photos: HTTP {response.status_code} - {response.text}"
            
    except httpx.TimeoutException:
        return "Error: Request timed out while retrieving photos. The content capture service may be slow or unavailable."
    except httpx.RequestError as e:
        return f"Error connecting to content capture service: {str(e)}"
    except Exception as e:
        return f"Unexpected error listing photos: {str(e)}"


@tool
def list_my_textbooks(class_id: Optional[int] = None, limit: int = 10) -> str:
    """List user's uploaded textbook PDFs and their processing status.
    
    Use this tool when the user wants to see their uploaded textbooks or check processing status.
    Textbooks can be filtered by class and results are paginated.
    
    Args:
        class_id: Optional class ID to filter textbooks (default: None = all classes)
        limit: Maximum number of textbooks to return (default: 10, max: 50)
    
    Returns:
        String with formatted list of textbooks including metadata and processing status, or error message.
    """
    try:
        params = {"limit": min(limit, 50)}
        if class_id:
            params["class_id"] = class_id
        
        response = httpx.get(
            f"{CONTENT_SERVICE_URL}/api/textbooks",
            params=params,
            timeout=10.0
        )
        
        if response.status_code == 200:
            data = response.json()
            textbooks = data.get("textbooks", [])
            total = data.get("total", 0)
            
            if not textbooks:
                return "No textbooks found. Upload textbook PDFs through the app to see them here."
            
            result = f"✓ Found {len(textbooks)} textbook(s) (Total: {total})\n\n"
            
            for book in textbooks:
                result += f"📚 Textbook ID: {book['id']}\n"
                result += f"  Title: {book['title']}\n"
                
                if book.get('author'):
                    result += f"  Author: {book['author']}\n"
                if book.get('isbn'):
                    result += f"  ISBN: {book['isbn']}\n"
                if book.get('class_id'):
                    result += f"  Class ID: {book['class_id']}\n"
                    
                result += f"  Pages: {book.get('page_count', 'unknown')}\n"
                result += f"  Chunks: {book.get('total_chunks', 0)}\n"
                result += f"  Status: {book['embedding_status']}\n"
                result += f"  Uploaded: {book.get('created_at', 'unknown')}\n\n"
            
            if any(book['embedding_status'] == 'pending' for book in textbooks):
                result += "ℹ️  Some textbooks are still being processed for AI search.\n"
            
            return result
            
        elif response.status_code == 401:
            return "Authentication required. This feature requires user authentication which is not yet integrated with agent tools."
        elif response.status_code == 404:
            return "Textbook service endpoint not found. The service may not be running."
        else:
            return f"Error retrieving textbooks: HTTP {response.status_code} - {response.text}"
            
    except httpx.TimeoutException:
        return "Error: Request timed out while retrieving textbooks. The content capture service may be slow or unavailable."
    except httpx.RequestError as e:
        return f"Error connecting to content capture service: {str(e)}"
    except Exception as e:
        return f"Unexpected error listing textbooks: {str(e)}"
