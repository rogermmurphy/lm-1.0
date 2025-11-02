"""
Data models for Class Management Service
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ClassBase(BaseModel):
    """Base class model"""
    name: str = Field(..., max_length=100)
    teacher_name: Optional[str] = Field(None, max_length=100)
    period: Optional[str] = Field(None, max_length=20)
    color: str = Field(default="#3B82F6", max_length=20)
    subject: Optional[str] = Field(None, max_length=50)
    current_grade: Optional[str] = Field(None, max_length=5)
    grade_percent: Optional[int] = Field(None, ge=0, le=100)


class ClassCreate(ClassBase):
    """Model for creating a class"""
    pass


class ClassUpdate(BaseModel):
    """Model for updating a class"""
    name: Optional[str] = Field(None, max_length=100)
    teacher_name: Optional[str] = Field(None, max_length=100)
    period: Optional[str] = Field(None, max_length=20)
    color: Optional[str] = Field(None, max_length=20)
    subject: Optional[str] = Field(None, max_length=50)
    current_grade: Optional[str] = Field(None, max_length=5)
    grade_percent: Optional[int] = Field(None, ge=0, le=100)


class Class(ClassBase):
    """Complete class model"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssignmentBase(BaseModel):
    """Base assignment model"""
    title: str = Field(..., max_length=200)
    type: str = Field(default="homework", max_length=50)
    description: Optional[str] = None
    due_date: datetime
    status: str = Field(default="pending", pattern="^(pending|in-progress|completed|overdue)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")


class AssignmentCreate(AssignmentBase):
    """Model for creating an assignment"""
    class_id: int


class AssignmentUpdate(BaseModel):
    """Model for updating an assignment"""
    title: Optional[str] = Field(None, max_length=200)
    type: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = Field(None, pattern="^(pending|in-progress|completed|overdue)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")


class Assignment(AssignmentBase):
    """Complete assignment model"""
    id: int
    class_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PlannerEventBase(BaseModel):
    """Base planner event model"""
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    event_type: str = Field(default="study", pattern="^(study|assignment|exam|class|other)$")
    start_time: datetime
    end_time: Optional[datetime] = None
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None
    is_completed: bool = False


class PlannerEventCreate(PlannerEventBase):
    """Model for creating a planner event"""
    class_id: Optional[int] = None
    assignment_id: Optional[int] = None


class PlannerEventUpdate(BaseModel):
    """Model for updating a planner event"""
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    event_type: Optional[str] = Field(None, pattern="^(study|assignment|exam|class|other)$")
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_rule: Optional[str] = None
    is_completed: Optional[bool] = None
    class_id: Optional[int] = None
    assignment_id: Optional[int] = None


class PlannerEvent(PlannerEventBase):
    """Complete planner event model"""
    id: int
    user_id: int
    class_id: Optional[int] = None
    assignment_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ClassScheduleBase(BaseModel):
    """Base class schedule model"""
    day_of_week: int = Field(..., ge=0, le=6)
    start_time: str  # TIME format "HH:MM:SS"
    end_time: str    # TIME format "HH:MM:SS"
    room_number: Optional[str] = Field(None, max_length=50)


class ClassScheduleCreate(ClassScheduleBase):
    """Model for creating a class schedule"""
    class_id: int


class ClassScheduleUpdate(BaseModel):
    """Model for updating a class schedule"""
    day_of_week: Optional[int] = Field(None, ge=0, le=6)
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    room_number: Optional[str] = Field(None, max_length=50)


class ClassSchedule(ClassScheduleBase):
    """Complete class schedule model"""
    id: int
    class_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
