"""
Database models for Gamification Service
"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


# ============================================================================
# USER POINTS
# ============================================================================

class UserPoints(BaseModel):
    id: int
    user_id: int
    total_points: int
    level: int
    streak_days: int
    last_activity_date: Optional[date]
    created_at: datetime
    updated_at: datetime


class PointAward(BaseModel):
    points: int
    reason: str
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None


# ============================================================================
# ACHIEVEMENTS
# ============================================================================

class Achievement(BaseModel):
    id: int
    user_id: int
    achievement_type: str
    achievement_name: str
    achievement_description: Optional[str]
    points_awarded: int
    earned_at: datetime


class AchievementCreate(BaseModel):
    achievement_type: str
    achievement_name: str
    achievement_description: Optional[str] = None
    points_awarded: int = 0


# ============================================================================
# LEADERBOARDS
# ============================================================================

class LeaderboardEntry(BaseModel):
    id: int
    leaderboard_type: str
    user_id: int
    score: int
    rank: Optional[int]
    period_start: Optional[date]
    period_end: Optional[date]
