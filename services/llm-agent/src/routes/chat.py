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
    ConversationCreateRequest,
    ConversationUpdateRequest,
    StudyMaterialUploadRequest,
    StudyMaterialResponse,
    MaterialsListResponse,
    MessageResponse,
    ChatSpeakRequest,
    ChatSpeakResponse,
    ChatTranscribeResponse
)
from ..services import RAGService, LLMService
from ..services.agent_service import AgentService
import requests
from fastapi import UploadFile, File
import time

router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize services (singleton pattern)
rag_service = RAGService()
llm_service = LLMService()

# Initialize agent service (with error handling for graceful fallback)
try:
    agent_service = AgentService()
    USE_AGENT = True
except Exception as e:
    print(f"Warning: AgentService initialization failed: {e}")
    print("Falling back to basic LLM service")
    agent_service = None
    USE_AGENT = False


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
    
    # Generate response using agent service (with fallback to basic LLM)
    try:
        if USE_AGENT and agent_service:
            # Use agent with tool capabilities
            response_text = agent_service.chat(
                message=request.message,
                conversation_history=conversation_history,
                use_rag=request.use_rag
            )
            sources = []  # Agent handles RAG internally
        else:
            # Fallback to basic LLM service
            context = ""
            sources = []
            if request.use_rag:
                try:
                    context, sources = rag_service.get_context_for_query(request.message, n_results=3)
                except Exception as e:
                    print(f"RAG retrieval failed: {e}")
            
            response_text = llm_service.chat_with_context(
                message=request.message,
                context=context,
                conversation_history=conversation_history
            )
    except Exception as e:
        import traceback
        print(f"Error generating response: {str(e)}")
        print(traceback.format_exc())
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


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    request: ConversationCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new conversation
    
    - **title**: Optional conversation title
    - **user_id**: User ID (TODO: Get from JWT token)
    """
    conversation = Conversation(
        user_id=request.user_id,
        title=request.title or "New Conversation"
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        message_count=0,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )


@router.put("/conversations/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: int,
    request: ConversationUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Update conversation title
    
    - **conversation_id**: Conversation ID
    - **title**: New conversation title
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    conversation.title = request.title
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conversation)
    
    message_count = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).count()
    
    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        message_count=message_count,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all messages for a conversation
    
    - **conversation_id**: Conversation ID
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()
    
    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    }


@router.delete("/conversations/{conversation_id}", response_model=MessageResponse)
async def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a conversation and all its messages
    
    - **conversation_id**: Conversation ID to delete
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Delete conversation (messages cascade automatically)
    db.delete(conversation)
    db.commit()
    
    return MessageResponse(message="Conversation deleted successfully")


@router.get("/materials", response_model=list[MaterialsListResponse])
async def list_materials(
    db: Session = Depends(get_db)
):
    """
    List user's study materials with content preview
    """
    # TODO: Filter by user_id from JWT token
    materials = db.query(StudyMaterial).order_by(
        StudyMaterial.created_at.desc()
    ).limit(50).all()
    
    result = []
    for material in materials:
        # Create content preview (first 200 characters)
        content_preview = material.content[:200] + "..." if len(material.content) > 200 else material.content
        
        result.append(MaterialsListResponse(
            id=material.id,
            title=material.title,
            subject=material.subject,
            content_preview=content_preview,
            created_at=material.created_at
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


@router.get("/voices")
async def get_available_voices():
    """
    Get list of available TTS voices
    
    Returns curated list of high-quality Azure TTS voices
    """
    # Curated list of best Azure voices based on POC 11 research
    voices = [
        {
            "id": "en-US-AriaNeural",
            "name": "Aria (Female, Clear)",
            "language": "English (US)",
            "gender": "Female",
            "description": "Clear and professional",
            "provider": "azure"
        },
        {
            "id": "en-US-JennyNeural",
            "name": "Jenny (Female, Friendly)",
            "language": "English (US)",
            "gender": "Female",
            "description": "Warm and conversational",
            "provider": "azure"
        },
        {
            "id": "en-US-GuyNeural",
            "name": "Guy (Male, Professional)",
            "language": "English (US)",
            "gender": "Male",
            "description": "Clear and professional",
            "provider": "azure"
        },
        {
            "id": "en-US-DavisNeural",
            "name": "Davis (Male, Confident)",
            "language": "English (US)",
            "gender": "Male",
            "description": "Expressive and confident",
            "provider": "azure"
        },
        {
            "id": "en-US-JaneNeural",
            "name": "Jane (Female, Natural)",
            "language": "English (US)",
            "gender": "Female",
            "description": "Natural and friendly",
            "provider": "azure"
        },
        {
            "id": "en-US-JasonNeural",
            "name": "Jason (Male, Casual)",
            "language": "English (US)",
            "gender": "Male",
            "description": "Casual and friendly",
            "provider": "azure"
        },
        {
            "id": "en-US-SaraNeural",
            "name": "Sara (Female, Soft)",
            "language": "English (US)",
            "gender": "Female",
            "description": "Soft and gentle",
            "provider": "azure"
        },
        {
            "id": "en-US-TonyNeural",
            "name": "Tony (Male, Narration)",
            "language": "English (US)",
            "gender": "Male",
            "description": "Professional narrator",
            "provider": "azure"
        }
    ]
    
    return {"voices": voices}


@router.post("/speak", response_model=ChatSpeakResponse)
async def speak_text(request: ChatSpeakRequest):
    """
    Convert text to speech using TTS service
    
    - **text**: Text to convert to speech
    - **voice**: Optional voice selection (default: en-US-AriaNeural)
    """
    try:
        # Call TTS service (container name: lm-tts, service name: tts-service)
        tts_url = "http://tts-service:8000/tts/generate"
        payload = {
            "text": request.text,
            "voice": request.voice or "en-US-AriaNeural"
        }
        
        response = requests.post(tts_url, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        return ChatSpeakResponse(
            success=True,
            audio_base64=data.get("audio_base64", ""),
            duration=None  # TTS doesn't return duration currently
        )
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"TTS service unavailable: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate speech: {str(e)}"
        )


@router.post("/transcribe", response_model=ChatTranscribeResponse)
async def transcribe_audio(audio_file: UploadFile = File(...)):
    """
    Transcribe audio to text using STT service
    
    - **audio_file**: Audio file to transcribe (mp3, wav, m4a, flac, ogg)
    """
    try:
        # Read audio file
        audio_content = await audio_file.read()
        
        # Send to STT service (container name: lm-stt, service name: stt-service)
        stt_url = "http://stt-service:8000/transcribe/"
        files = {"file": (audio_file.filename, audio_content, audio_file.content_type)}
        data = {"language": "en"}
        
        response = requests.post(stt_url, files=files, data=data, timeout=10)
        response.raise_for_status()
        
        job_data = response.json()
        job_id = job_data.get("job_id")
        
        # Poll for result (max 30 seconds)
        max_attempts = 15
        for attempt in range(max_attempts):
            time.sleep(2)  # Wait 2 seconds between polls
            
            status_url = f"http://stt-service:8000/transcribe/jobs/{job_id}"
            status_response = requests.get(status_url, timeout=5)
            status_response.raise_for_status()
            
            status_data = status_response.json()
            
            if status_data.get("status") == "completed":
                # Get transcription result
                result_url = f"http://stt-service:8000/transcribe/results/{job_id}"
                result_response = requests.get(result_url, timeout=5)
                result_response.raise_for_status()
                
                result_data = result_response.json()
                transcription_text = result_data.get("transcription_text", "")
                
                return ChatTranscribeResponse(
                    success=True,
                    text=transcription_text,
                    job_id=str(job_id)
                )
            
            elif status_data.get("status") == "failed":
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Transcription failed"
                )
        
        # Timeout - return job ID for client to poll
        return ChatTranscribeResponse(
            success=False,
            text="Transcription is still processing. Please try again in a few seconds.",
            job_id=str(job_id)
        )
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"STT service unavailable: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to transcribe audio: {str(e)}"
        )
