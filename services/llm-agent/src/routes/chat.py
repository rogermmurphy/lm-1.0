"""
LLM Agent Service - Chat Routes
API endpoints for AI chat interactions
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from lm_common.database import get_db

from ..models import Conversation, Message, StudyMaterial
from ..schemas import (
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationResponse,
    StudyMaterialUploadRequest,
    StudyMaterialResponse
)
from ..services import RAGService, LLMService

router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize services (singleton pattern)
rag_service = RAGService()
llm_service = LLMService()


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    db: Session = Depends(get_db)
):
    """
    Send a message to the AI tutor
    
    - **conversation_id**: Optional conversation ID (creates new if not provided)
    - **message**: User message
    - **use_rag**: Whether to use RAG context retrieval
    """
    # Get or create conversation
    if request.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == request.conversation_id
        ).first()
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        # Create new conversation
        conversation = Conversation(
            user_id=1,  # TODO: Get from JWT token
            title=request.message[:50] + "..." if len(request.message) > 50 else request.message
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    
    # Store user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    db.add(user_message)
    
    # Get conversation history
    history_messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()
    
    conversation_history = [
        {"role": msg.role, "content": msg.content}
        for msg in history_messages
    ]
    
    # Get RAG context if enabled
    context = ""
    sources = []
    if request.use_rag:
        try:
            context, sources = rag_service.get_context_for_query(request.message, n_results=3)
        except Exception as e:
            print(f"RAG retrieval failed: {e}")
    
    # Generate response
    try:
        response_text = llm_service.chat_with_context(
            message=request.message,
            context=context,
            conversation_history=conversation_history
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate response: {str(e)}"
        )
    
    # Store assistant message
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=response_text
    )
    db.add(assistant_message)
    
    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(assistant_message)
    
    # Format sources
    source_list = [s['source'] for s in sources] if sources else None
    
    return ChatMessageResponse(
        conversation_id=conversation.id,
        message_id=assistant_message.id,
        response=response_text,
        sources=source_list,
        created_at=assistant_message.created_at
    )


@router.get("/conversations", response_model=list[ConversationResponse])
async def list_conversations(
    db: Session = Depends(get_db)
):
    """List user's conversations"""
    # TODO: Filter by user_id from JWT token
    conversations = db.query(Conversation).order_by(
        Conversation.updated_at.desc()
    ).limit(50).all()
    
    result = []
    for conv in conversations:
        message_count = db.query(Message).filter(
            Message.conversation_id == conv.id
        ).count()
        
        result.append(ConversationResponse(
            id=conv.id,
            title=conv.title,
            message_count=message_count,
            created_at=conv.created_at,
            updated_at=conv.updated_at
        ))
    
    return result


@router.post("/materials", response_model=StudyMaterialResponse)
async def upload_study_material(
    request: StudyMaterialUploadRequest,
    db: Session = Depends(get_db)
):
    """
    Upload study material and add to vector database
    
    - **title**: Material title
    - **content**: Text content
    - **subject**: Optional subject/topic
    """
    # Create study material record
    material = StudyMaterial(
        user_id=1,  # TODO: Get from JWT token
        title=request.title,
        content=request.content,
        subject=request.subject
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    
    # Add to vector database
    try:
        metadata = {
            "user_id": material.user_id,
            "material_id": material.id,
            "title": material.title,
            "subject": material.subject or "general",
            "source": material.title
        }
        rag_service.add_document(
            text=request.content,
            metadata=metadata
        )
    except Exception as e:
        # Rollback database if vector storage fails
        db.delete(material)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add to vector database: {str(e)}"
        )
    
    return StudyMaterialResponse(
        id=material.id,
        title=material.title,
        subject=material.subject,
        created_at=material.created_at
    )
