from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Notification Models
class NotificationCreate(BaseModel):
    user_id: int
    type: str
    title: str
    message: str
    related_id: Optional[int] = None
    related_type: Optional[str] = None
    action_url: Optional[str] = None

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    title: str
    message: str
    related_id: Optional[int]
    related_type: Optional[str]
    action_url: Optional[str]
    is_read: bool
    read_at: Optional[datetime]
    created_at: datetime

class NotificationMarkRead(BaseModel):
    notification_ids: List[int]

class NotificationPreferences(BaseModel):
    email_enabled: bool = True
    push_enabled: bool = True
    assignment_notifications: bool = True
    grade_notifications: bool = True
    message_notifications: bool = True
    social_notifications: bool = True
    achievement_notifications: bool = True

class NotificationPreferencesResponse(BaseModel):
    user_id: int
    email_enabled: bool
    push_enabled: bool
    assignment_notifications: bool
    grade_notifications: bool
    message_notifications: bool
    social_notifications: bool
    achievement_notifications: bool
    updated_at: datetime

# Message Models
class MessageSend(BaseModel):
    recipient_id: int
    message: str

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    message: str
    is_read: bool
    read_at: Optional[datetime]
    created_at: datetime

class ConversationResponse(BaseModel):
    user_id: int
    user_name: str
    last_message: str
    last_message_time: datetime
    unread_count: int

class MessageMarkRead(BaseModel):
    message_ids: List[int]
