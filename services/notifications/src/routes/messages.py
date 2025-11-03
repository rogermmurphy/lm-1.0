from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models import MessageSend, MessageResponse, ConversationResponse, MessageMarkRead
from ..services.message_service import MessageService

router = APIRouter(prefix="/api/messages", tags=["messages"])
message_service = MessageService()

# Mock auth dependency - replace with real JWT validation
def get_current_user_id():
    return 7  # Test user

@router.post("/send", response_model=MessageResponse)
async def send_message(
    data: MessageSend,
    user_id: int = Depends(get_current_user_id)
):
    """Send a direct message"""
    try:
        message = message_service.send_message(user_id, data.recipient_id, data.message)
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(user_id: int = Depends(get_current_user_id)):
    """List all conversations for the current user"""
    try:
        conversations = message_service.get_conversations(user_id)
        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversation/{other_user_id}", response_model=List[MessageResponse])
async def get_conversation(
    other_user_id: int,
    limit: int = 50,
    user_id: int = Depends(get_current_user_id)
):
    """Get messages in a conversation with another user"""
    try:
        messages = message_service.get_conversation(user_id, other_user_id, limit)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mark-read")
async def mark_messages_read(
    data: MessageMarkRead,
    user_id: int = Depends(get_current_user_id)
):
    """Mark messages as read"""
    try:
        count = message_service.mark_messages_as_read(user_id, data.message_ids)
        return {"message": f"Marked {count} messages as read", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """Delete a message (only if sender)"""
    try:
        success = message_service.delete_message(user_id, message_id)
        if not success:
            raise HTTPException(status_code=404, detail="Message not found or not authorized")
        return {"message": "Message deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
