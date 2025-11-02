"""
Content Capture Service - Photo Routes
Handles photo upload, OCR processing, and vector embedding
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import shutil
from PIL import Image
import pytesseract

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from lm_common.database import get_db
from lm_common.auth.jwt_utils import decode_token
from models import Photo
from services.ocr_service import OCRService
from services.vector_service import VectorService
from config import settings

router = APIRouter()
security = HTTPBearer()

# Initialize services
ocr_service = OCRService()
vector_service = VectorService()

@router.post("/photos/upload")
async def upload_photo(
    file: UploadFile = File(...),
    title: str = Form(...),
    class_id: Optional[int] = Form(None),
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Upload and process a photo with OCR"""
    
    # Verify JWT token
    payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    
    # Validate file type
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed types: {settings.ALLOWED_IMAGE_TYPES}"
        )
    
    # Validate file size
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE} bytes"
        )
    
    try:
        # Create upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create photo record
        photo = Photo(
            user_id=user_id,
            class_id=class_id,
            title=title,
            image_url=file_path,
            extraction_status="pending"
        )
        
        db.add(photo)
        db.commit()
        db.refresh(photo)
        
        # Start OCR processing asynchronously
        try:
            extracted_text = await ocr_service.extract_text(file_path)
            
            # Update photo with extracted text
            photo.extracted_text = extracted_text
            photo.extraction_status = "completed"
            
            # Create vector embedding if text was extracted
            if extracted_text and extracted_text.strip():
                vector_id = await vector_service.create_embedding(
                    text=extracted_text,
                    metadata={
                        "type": "photo",
                        "photo_id": photo.id,
                        "class_id": class_id,
                        "user_id": user_id,
                        "title": title
                    }
                )
                photo.vector_id = vector_id
            
            db.commit()
            
        except Exception as ocr_error:
            photo.extraction_status = "failed"
            db.commit()
            print(f"OCR processing failed: {ocr_error}")
        
        return {
            "id": photo.id,
            "title": photo.title,
            "image_url": photo.image_url,
            "extracted_text": photo.extracted_text,
            "extraction_status": photo.extraction_status,
            "class_id": photo.class_id,
            "created_at": photo.created_at
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/photos")
async def get_photos(
    class_id: Optional[int] = None,
    limit: int = 20,
    offset: int = 0,
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Get user's photos with optional class filter"""
    
    # Verify JWT token
    payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    
    # Build query
    query = db.query(Photo).filter(Photo.user_id == user_id)
    
    if class_id:
        query = query.filter(Photo.class_id == class_id)
    
    # Get photos with pagination
    photos = query.order_by(Photo.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "photos": [
            {
                "id": photo.id,
                "title": photo.title,
                "image_url": photo.image_url,
                "extracted_text": photo.extracted_text,
                "extraction_status": photo.extraction_status,
                "class_id": photo.class_id,
                "created_at": photo.created_at
            }
            for photo in photos
        ],
        "total": query.count(),
        "limit": limit,
        "offset": offset
    }

@router.get("/photos/{photo_id}")
async def get_photo(
    photo_id: int,
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Get a specific photo by ID"""
    
    # Verify JWT token
    payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    
    # Get photo
    photo = db.query(Photo).filter(
        Photo.id == photo_id,
        Photo.user_id == user_id
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    return {
        "id": photo.id,
        "title": photo.title,
        "image_url": photo.image_url,
        "extracted_text": photo.extracted_text,
        "extraction_status": photo.extraction_status,
        "class_id": photo.class_id,
        "vector_id": photo.vector_id,
        "created_at": photo.created_at,
        "updated_at": photo.updated_at
    }

@router.put("/photos/{photo_id}")
async def update_photo(
    photo_id: int,
    title: Optional[str] = None,
    class_id: Optional[int] = None,
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Update photo metadata"""
    
    # Verify JWT token
    payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    
    # Get photo
    photo = db.query(Photo).filter(
        Photo.id == photo_id,
        Photo.user_id == user_id
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    # Update fields
    if title is not None:
        photo.title = title
    if class_id is not None:
        photo.class_id = class_id
    
    db.commit()
    db.refresh(photo)
    
    return {
        "id": photo.id,
        "title": photo.title,
        "class_id": photo.class_id,
        "updated_at": photo.updated_at
    }

@router.delete("/photos/{photo_id}")
async def delete_photo(
    photo_id: int,
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Delete a photo"""
    
    # Verify JWT token
    payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    
    # Get photo
    photo = db.query(Photo).filter(
        Photo.id == photo_id,
        Photo.user_id == user_id
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    # Delete file from filesystem
    try:
        if os.path.exists(photo.image_url):
            os.remove(photo.image_url)
    except Exception as e:
        print(f"Failed to delete file: {e}")
    
    # Delete vector embedding
    if photo.vector_id:
        try:
            await vector_service.delete_embedding(photo.vector_id)
        except Exception as e:
            print(f"Failed to delete vector: {e}")
    
    # Delete from database
    db.delete(photo)
    db.commit()
    
    return {"message": "Photo deleted successfully"}

@router.post("/photos/{photo_id}/reprocess")
async def reprocess_photo(
    photo_id: int,
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Reprocess photo OCR and vector embedding"""
    
    # Verify JWT token
    payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    
    # Get photo
    photo = db.query(Photo).filter(
        Photo.id == photo_id,
        Photo.user_id == user_id
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    try:
        # Update status
        photo.extraction_status = "processing"
        db.commit()
        
        # Reprocess OCR
        extracted_text = await ocr_service.extract_text(photo.image_url)
        
        # Delete old vector if exists
        if photo.vector_id:
            await vector_service.delete_embedding(photo.vector_id)
        
        # Update photo
        photo.extracted_text = extracted_text
        photo.extraction_status = "completed"
        photo.vector_id = None
        
        # Create new vector embedding
        if extracted_text and extracted_text.strip():
            vector_id = await vector_service.create_embedding(
                text=extracted_text,
                metadata={
                    "type": "photo",
                    "photo_id": photo.id,
                    "class_id": photo.class_id,
                    "user_id": user_id,
                    "title": photo.title
                }
            )
            photo.vector_id = vector_id
        
        db.commit()
        
        return {
            "id": photo.id,
            "extracted_text": photo.extracted_text,
            "extraction_status": photo.extraction_status,
            "vector_id": photo.vector_id
        }
        
    except Exception as e:
        photo.extraction_status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Reprocessing failed: {str(e)}")
