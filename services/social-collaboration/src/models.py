"""
Database models for Social & Collaboration Service
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# ============================================================================
# CLASSMATE CONNECTIONS
# ============================================================================

class ConnectionCreate(BaseModel):
    classmate_user_id: int

class ConnectionUpdate(BaseModel):
    status: str  # 'accepted', 'rejected', 'blocked'

class Connection(BaseModel):
    id: int
    user_id: int
    classmate_user_id: int
    status: str
    created_at: datetime
    updated_at: datetime


# ============================================================================
# SHARED CONTENT
# ============================================================================

class SharedContentCreate(BaseModel):
    content_type: str  # 'note', 'flashcard_deck', 'test', 'recording', 'photo', 'textbook'
    content_id: int
    shared_with_user_id: int
    permissions: str = 'view'  # 'view', 'edit', 'admin'

class SharedContent(BaseModel):
    id: int
    content_type: str
    content_id: int
    shared_by_user_id: int
    shared_with_user_id: int
    permissions: str
    created_at: datetime


# ============================================================================
# STUDY GROUPS
# ============================================================================

class StudyGroupCreate(BaseModel):
    name: str
    description: Optional[str] = None
    class_id: Optional[int] = None
    max_members: int = 10

class StudyGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    max_members: Optional[int] = None

class StudyGroup(BaseModel):
    id: int
    name: str
    description: Optional[str]
    class_id: Optional[int]
    created_by_user_id: int
    is_active: bool
    max_members: int
    created_at: datetime
    updated_at: datetime


# ============================================================================
# STUDY GROUP MEMBERS
# ============================================================================

class GroupMemberAdd(BaseModel):
    user_id: int
    role: str = 'member'  # 'admin', 'moderator', 'member'

class GroupMemberUpdate(BaseModel):
    role: str

class GroupMember(BaseModel):
    id: int
    group_id: int
    user_id: int
    role: str
    joined_at: datetime


# ============================================================================
# STUDY GROUP MESSAGES
# ============================================================================

class GroupMessageCreate(BaseModel):
    message_text: str

class GroupMessage(BaseModel):
    id: int
    group_id: int
    user_id: int
    message_text: str
    is_deleted: bool
    created_at: datetime
