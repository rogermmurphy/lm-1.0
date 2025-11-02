"""
Content Capture Service - Textbook Routes
Handles textbook upload, PDF processing, and chunking for vector search
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import shutil
import PyPDF2
from io import BytesIO

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from lm_common.database import get_db
from lm_common.auth.jwt_utils import decode_token
from models import TextbookDownload, TextbookChunk
from services.vector_service import VectorService
from services.pdf_processor import PDFProcessor
from config import settings

router = APIRouter()
security = HTTPBearer()

# Initialize services
vector_service = VectorService()
pdf_processor = PDFProcessor()

@router.post("/textbooks/upload")
async def upload_textbook(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: Optional[str] = Form(None),
    isbn: Optional[str] = Form(None),
    class_id: Optional[int] = Form(None),
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Upload and process a textbook PDF"""
    
    # Verify JWT token
    payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    
    # Validate file type
    if file.content_type not in settings.ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed types: {settings.ALLOWED_DOCUMENT_TYPES}"
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
        
        # Get basic PDF info
        pdf_info = pdf_processor.get_pdf_info(file_path)
        
        # Create textbook record
        textbook = TextbookDownload(
            user_id=user_id,
            class_id=class_id,
            title=title,
            author=author,
            isbn=isbn,
            file_url=file_path,
            file_type="pdf",
            file_size_bytes=file.size,
            page_count=pdf_info.get("page_count", 0),
            embedding_status="pending"
        )
        
        db.add(textbook)
        db.commit()
        db.refresh(textbook)
        
        # Start processing asynchronously
        try:
            # Extract and chunk text
            chunks = await pdf_processor.extract_and_chunk(file_path)
            
            # Create vector embeddings for each chunk
            chunk_records = []
            for i, chunk_data in enumerate(chunks):
                # Create chunk record
                chunk = TextbookChunk(
                    textbook_id=textbook.id,
                    chunk_index=i,
                    page_number=chunk_data.get("page_number"),
                    content=chunk_data["content"]
                )
                
                # Create vector embedding
                if chunk_data["content"].strip():
                    vector_id = await vector_service.create_embedding(
                        text=chunk_data["content"],
                        metadata={
                            "type": "textbook",
                            "textbook_id": textbook.id,
                            "chunk_id": chunk.id,
                            "class_id": class_id,
                            "user_id": user_id,
                            "title": title,
                            "page_number": chunk_data.get("page_number")
                        }
                    )
                    chunk.vector_id = vector_id
                
                chunk_records.append(chunk)
            
            # Save all chunks
            db.add_all(chunk_records)
            
            # Update textbook status
            textbook.total_chunks = len(chunk_records)
            textbook.embedding_status = "completed"
            
            db.commit()
            
        except Exception as processing_error:
            textbook.embedding_status = "failed"
            db.commit()
            print(f"Textbook processing failed: {processing_error}")
        
        return {
            "id": textbook.id,
            "title": textbook.title,
            "author": textbook.author,
            "isbn": textbook.isbn,
            "file_url": textbook.file_url,
            "page_count": textbook.page_count,
            "total_chunks": textbook.total_chunks,
            "embedding_status": textbook.embedding_status,
            "class_id": textbook.class_id,
            "created_at": textbook.created_at
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/textbooks")
async def get_textbooks(
    class_id: Optional[int] = None,
    limit: int = 20,
    offset: int = 0,
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Get user's textbooks with optional class filter"""
    
    # Verify JWT token
    payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    
    # Build query
    query = db.query(TextbookDownload).filter(TextbookDownload.user_id == user_id)
    
    if class_id:
        query = query.filter(TextbookDownload.class_id == class_id)
    
    # Get textbooks with pagination
    textbooks = query.order_by(TextbookDownload.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "textbooks": [
            {
                "id": textbook.id,
                "title": textbook.title,
                "author": textbook.author,
                "isbn": textbook.isbn,
                "file_url": textbook.file_url,
                "page_count": textbook.page_count,
                "total_chunks": textbook.total_chunks,
                "embedding_status": textbook.embedding_status,
                "class_id": textbook.class_id,
                "created_at": textbook.created_at
            }
            for textbook in textbooks
        ],
        "total": query.count(),
        "limit": limit,
        "offset": offset
    }

@router.get("/textbooks/{textbook_id}")
async def get_textbook(
    textbook_id: int,
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Get a specific textbook by ID"""
    
    # Verify JWT token
    payload = verify_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    # Get textbook
    textbook = db.query(TextbookDownload).filter(
        TextbookDownload.id == textbook_id,
        TextbookDownload.user_id == user_id
    ).first()
    
    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")
    
    return {
        "id": textbook.id,
        "title": textbook.title,
        "author": textbook.author,
        "isbn": textbook.isbn,
        "file_url": textbook.file_url,
        "file_type": textbook.file_type,
        "file_size_bytes": textbook.file_size_bytes,
        "page_count": textbook.page_count,
        "total_chunks": textbook.total_chunks,
        "embedding_status": textbook.embedding_status,
        "class_id": textbook.class_id,
        "created_at": textbook.created_at,
        "updated_at": textbook.updated_at
    }

@router.get("/textbooks/{textbook_id}/chunks")
async def get_textbook_chunks(
    textbook_id: int,
    page_number: Optional[int] = None,
    limit: int = 20,
    offset: int = 0,
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Get chunks for a specific textbook"""
    
    # Verify JWT token
    payload = verify_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    # Verify textbook ownership
    textbook = db.query(TextbookDownload).filter(
        TextbookDownload.id == textbook_id,
        TextbookDownload.user_id == user_id
    ).first()
    
    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")
    
    # Build query for chunks
    query = db.query(TextbookChunk).filter(TextbookChunk.textbook_id == textbook_id)
    
    if page_number:
        query = query.filter(TextbookChunk.page_number == page_number)
    
    # Get chunks with pagination
    chunks = query.order_by(TextbookChunk.chunk_index).offset(offset).limit(limit).all()
    
    return {
        "chunks": [
            {
                "id": chunk.id,
                "chunk_index": chunk.chunk_index,
                "page_number": chunk.page_number,
                "content": chunk.content,
                "vector_id": chunk.vector_id,
                "created_at": chunk.created_at
            }
            for chunk in chunks
        ],
        "total": query.count(),
        "limit": limit,
        "offset": offset
    }

@router.post("/textbooks/search")
async def search_textbooks(
    query: str,
    class_id: Optional[int] = None,
    textbook_id: Optional[int] = None,
    limit: int = 10,
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Search textbook content using vector similarity"""
    
    # Verify JWT token
    payload = verify_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    # Build filters
    filters = {
        "type": "textbook",
        "user_id": str(user_id)
    }
    
    if class_id:
        filters["class_id"] = str(class_id)
    
    if textbook_id:
        filters["textbook_id"] = str(textbook_id)
    
    # Search using vector service
    results = await vector_service.search_similar(
        query_text=query,
        limit=limit,
        filters=filters
    )
    
    # Enrich results with textbook information
    enriched_results = []
    for result in results:
        metadata = result["metadata"]
        
        # Get textbook info if available
        textbook_info = None
        if "textbook_id" in metadata:
            textbook = db.query(TextbookDownload).filter(
                TextbookDownload.id == int(metadata["textbook_id"])
            ).first()
            
            if textbook:
                textbook_info = {
                    "id": textbook.id,
                    "title": textbook.title,
                    "author": textbook.author
                }
        
        enriched_results.append({
            "content": result["document"],
            "similarity": result["similarity"],
            "metadata": metadata,
            "textbook": textbook_info
        })
    
    return {
        "query": query,
        "results": enriched_results,
        "total": len(enriched_results)
    }

@router.delete("/textbooks/{textbook_id}")
async def delete_textbook(
    textbook_id: int,
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Delete a textbook and all its chunks"""
    
    # Verify JWT token
    payload = verify_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    # Get textbook
    textbook = db.query(TextbookDownload).filter(
        TextbookDownload.id == textbook_id,
        TextbookDownload.user_id == user_id
    ).first()
    
    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")
    
    # Delete file from filesystem
    try:
        if os.path.exists(textbook.file_url):
            os.remove(textbook.file_url)
    except Exception as e:
        print(f"Failed to delete file: {e}")
    
    # Delete vector embeddings for all chunks
    chunks = db.query(TextbookChunk).filter(TextbookChunk.textbook_id == textbook_id).all()
    for chunk in chunks:
        if chunk.vector_id:
            try:
                await vector_service.delete_embedding(chunk.vector_id)
            except Exception as e:
                print(f"Failed to delete vector: {e}")
    
    # Delete from database (cascades to chunks)
    db.delete(textbook)
    db.commit()
    
    return {"message": "Textbook deleted successfully"}

@router.post("/textbooks/{textbook_id}/reprocess")
async def reprocess_textbook(
    textbook_id: int,
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Reprocess textbook chunks and vector embeddings"""
    
    # Verify JWT token
    payload = verify_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    # Get textbook
    textbook = db.query(TextbookDownload).filter(
        TextbookDownload.id == textbook_id,
        TextbookDownload.user_id == user_id
    ).first()
    
    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")
    
    try:
        # Update status
        textbook.embedding_status = "processing"
        db.commit()
        
        # Delete existing chunks and their vectors
        existing_chunks = db.query(TextbookChunk).filter(TextbookChunk.textbook_id == textbook_id).all()
        for chunk in existing_chunks:
            if chunk.vector_id:
                await vector_service.delete_embedding(chunk.vector_id)
        
        # Delete chunk records
        db.query(TextbookChunk).filter(TextbookChunk.textbook_id == textbook_id).delete()
        db.commit()
        
        # Reprocess PDF
        chunks = await pdf_processor.extract_and_chunk(textbook.file_url)
        
        # Create new chunks and embeddings
        chunk_records = []
        for i, chunk_data in enumerate(chunks):
            chunk = TextbookChunk(
                textbook_id=textbook.id,
                chunk_index=i,
                page_number=chunk_data.get("page_number"),
                content=chunk_data["content"]
            )
            
            if chunk_data["content"].strip():
                vector_id = await vector_service.create_embedding(
                    text=chunk_data["content"],
                    metadata={
                        "type": "textbook",
                        "textbook_id": textbook.id,
                        "chunk_id": chunk.id,
                        "class_id": textbook.class_id,
                        "user_id": user_id,
                        "title": textbook.title,
                        "page_number": chunk_data.get("page_number")
                    }
                )
                chunk.vector_id = vector_id
            
            chunk_records.append(chunk)
        
        # Save new chunks
        db.add_all(chunk_records)
        
        # Update textbook
        textbook.total_chunks = len(chunk_records)
        textbook.embedding_status = "completed"
        
        db.commit()
        
        return {
            "id": textbook.id,
            "total_chunks": textbook.total_chunks,
            "embedding_status": textbook.embedding_status
        }
        
    except Exception as e:
        textbook.embedding_status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Reprocessing failed: {str(e)}")
