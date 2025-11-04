from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models import (
    NotificationResponse, NotificationMarkRead, NotificationPreferences,
    NotificationPreferencesResponse
)
from ..services.notification_service import NotificationService

router = APIRouter(prefix="/api/notifications", tags=["notifications"])
notification_service = NotificationService()

# Mock auth dependency - replace with real JWT validation
def get_current_user_id():
    return 7  # Test user

@router.get("/", response_model=List[NotificationResponse])
async def list_notifications(
    limit: int = 50,
    offset: int = 0,
    user_id: int = Depends(get_current_user_id)
):
    """List notifications for the current user"""
    try:
        notifications = notification_service.list_notifications(user_id, limit, offset)
        return notifications
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mark-read")
async def mark_notifications_read(
    data: NotificationMarkRead,
    user_id: int = Depends(get_current_user_id)
):
    """Mark specific notifications as read"""
    try:
        count = notification_service.mark_as_read(user_id, data.notification_ids)
        return {"message": f"Marked {count} notifications as read", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mark-all-read")
async def mark_all_notifications_read(user_id: int = Depends(get_current_user_id)):
    """Mark all notifications as read"""
    try:
        count = notification_service.mark_all_as_read(user_id)
        return {"message": f"Marked {count} notifications as read", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """Delete a notification"""
    try:
        success = notification_service.delete_notification(user_id, notification_id)
        if not success:
            raise HTTPException(status_code=404, detail="Notification not found")
        return {"message": "Notification deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/unread-count")
async def get_unread_count(user_id: int = Depends(get_current_user_id)):
    """Get count of unread notifications"""
    try:
        count = notification_service.get_unread_count(user_id)
        return {"unread_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preferences", response_model=NotificationPreferencesResponse)
async def get_notification_preferences(user_id: int = Depends(get_current_user_id)):
    """Get notification preferences"""
    try:
        preferences = notification_service.get_preferences(user_id)
        return preferences
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/preferences", response_model=NotificationPreferencesResponse)
async def update_notification_preferences(
    preferences: NotificationPreferences,
    user_id: int = Depends(get_current_user_id)
):
    """Update notification preferences"""
    try:
        updated = notification_service.update_preferences(
            user_id,
            preferences.model_dump(exclude_unset=True)
        )
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
