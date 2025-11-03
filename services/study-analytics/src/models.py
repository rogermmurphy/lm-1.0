"""
Pydantic models for Study Analytics Service
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal

# ============================================================================
# Study Session Models
# ============================================================================

class SessionStart(BaseModel):
    """Request model for starting a study session"""
    class_id: Optional[int] = None
    session_type: str = Field(..., pattern="^(solo|group|tutoring)$")
    focus_mode: bool = False
    location: Optional[str] = None

class SessionEnd(BaseModel):
    """Request model for ending a study session"""
    mood_rating: Optional[int] = Field(None, ge=1, le=5)
    productivity_rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None

class ActivityLog(BaseModel):
    """Request model for logging an activity"""
    activity_type: str = Field(..., pattern="^(reading|testing|flashcards|notes|video|chat|assignment)$")
    content_type: Optional[str] = None
    content_id: Optional[int] = None
    items_completed: int = 0
    items_correct: Optional[int] = None
    duration_minutes: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class StudySession(BaseModel):
    """Response model for a study session"""
    id: int
    user_id: int
    class_id: Optional[int]
    class_name: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime]
    duration_minutes: Optional[int]
    session_type: str
    focus_mode: bool
    location: Optional[str]
    notes: Optional[str]
    mood_rating: Optional[int]
    productivity_rating: Optional[int]
    created_at: datetime
    updated_at: datetime

class SessionActivity(BaseModel):
    """Response model for a session activity"""
    id: int
    session_id: int
    activity_type: str
    content_type: Optional[str]
    content_id: Optional[int]
    start_time: datetime
    end_time: Optional[datetime]
    duration_minutes: Optional[int]
    items_completed: int
    items_correct: Optional[int]
    accuracy_percentage: Optional[Decimal]
    points_earned: int
    metadata: Optional[Dict[str, Any]]
    created_at: datetime

# ============================================================================
# Performance Models
# ============================================================================

class PerformanceOverview(BaseModel):
    """Response model for performance overview"""
    user_id: int
    period: str
    period_start: date
    period_end: date
    metrics: Dict[str, Any]
    strengths: List[str]
    areas_for_improvement: List[str]
    recommendations: List[str]

class PerformanceTrend(BaseModel):
    """Response model for performance trends"""
    metric_type: str
    data_points: List[Dict[str, Any]]
    overall_trend: str
    trend_percentage: Optional[Decimal]

class PerformanceComparison(BaseModel):
    """Response model for performance comparison"""
    comparison_type: str
    period: str
    comparisons: List[Dict[str, Any]]

# ============================================================================
# Goal Models
# ============================================================================

class GoalCreate(BaseModel):
    """Request model for creating a goal"""
    class_id: Optional[int] = None
    goal_type: str = Field(..., pattern="^(study_time|test_score|assignment_completion|flashcard_mastery|streak|custom)$")
    goal_name: str = Field(..., min_length=1, max_length=200)
    goal_description: Optional[str] = None
    target_value: Decimal = Field(..., gt=0)
    unit: Optional[str] = None
    start_date: date
    target_date: date
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    reminder_enabled: bool = True
    
    @field_validator('target_date')
    @classmethod
    def validate_dates(cls, v, info):
        if 'start_date' in info.data and v < info.data['start_date']:
            raise ValueError('target_date must be >= start_date')
        return v

class GoalUpdate(BaseModel):
    """Request model for updating a goal"""
    goal_name: Optional[str] = Field(None, min_length=1, max_length=200)
    goal_description: Optional[str] = None
    target_value: Optional[Decimal] = Field(None, gt=0)
    target_date: Optional[date] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    reminder_enabled: Optional[bool] = None
    status: Optional[str] = Field(None, pattern="^(active|completed|abandoned|expired)$")

class GoalProgressRecord(BaseModel):
    """Request model for recording goal progress"""
    progress_value: Decimal = Field(..., ge=0)
    notes: Optional[str] = None

class StudyGoal(BaseModel):
    """Response model for a study goal"""
    id: int
    user_id: int
    class_id: Optional[int]
    goal_type: str
    goal_name: str
    goal_description: Optional[str]
    target_value: Decimal
    current_value: Decimal
    unit: Optional[str]
    start_date: date
    target_date: date
    status: str
    priority: str
    is_recurring: bool
    recurrence_pattern: Optional[str]
    reminder_enabled: bool
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    # Calculated fields
    percentage_complete: Optional[Decimal] = None
    days_remaining: Optional[int] = None
    on_track: Optional[bool] = None

class GoalProgress(BaseModel):
    """Response model for goal progress"""
    id: int
    goal_id: int
    recorded_date: date
    progress_value: Decimal
    percentage_complete: Optional[Decimal]
    notes: Optional[str]
    milestone_reached: bool
    milestone_name: Optional[str]
    created_at: datetime

# ============================================================================
# Report Models
# ============================================================================

class DailyReport(BaseModel):
    """Response model for daily study report"""
    date: date
    summary: Dict[str, Any]
    sessions: List[StudySession]
    achievements_earned: List[Dict[str, Any]]
    goals_progress: List[Dict[str, Any]]

class WeeklyReport(BaseModel):
    """Response model for weekly study report"""
    week: str  # Format: 2025-W44
    week_start: date
    week_end: date
    summary: Dict[str, Any]
    daily_breakdown: List[Dict[str, Any]]
    top_subjects: List[Dict[str, Any]]
    performance_highlights: List[str]

class MonthlyReport(BaseModel):
    """Response model for monthly study report"""
    month: str  # Format: 2025-11
    summary: Dict[str, Any]
    performance_summary: Dict[str, Any]
    goals_achieved: List[StudyGoal]
    top_achievements: List[Dict[str, Any]]
    recommendations: List[str]

# ============================================================================
# Common Response Models
# ============================================================================

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    data: Optional[Dict[str, Any]] = None

class SessionsListResponse(BaseModel):
    """Response model for sessions list"""
    sessions: List[StudySession]
    total_count: int
    total_minutes: int
    avg_duration: Optional[int]

class GoalsListResponse(BaseModel):
    """Response model for goals list"""
    goals: List[StudyGoal]
    total_count: int
    active_count: int
    completed_count: int
