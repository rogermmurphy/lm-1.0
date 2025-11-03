"""
Pydantic models for AI Study Tools Service
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class SourceType(str, Enum):
    RECORDING = "recording"
    PHOTO = "photo"
    TEXTBOOK = "textbook"
    MANUAL = "manual"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"


# ============================================================================
# NOTE MODELS
# ============================================================================

class NoteGenerateRequest(BaseModel):
    source_type: SourceType
    source_id: int
    class_id: Optional[int] = None
    user_id: int


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    is_ai_generated: bool
    class_id: Optional[int]
    created_at: datetime


# ============================================================================
# TEST MODELS
# ============================================================================

class TestGenerateRequest(BaseModel):
    class_id: Optional[int] = None
    user_id: int
    title: str
    description: Optional[str] = None
    difficulty: Difficulty = Difficulty.MEDIUM
    question_count: int = Field(default=10, ge=1, le=50)
    source_material_ids: List[int] = []


class QuestionOption(BaseModel):
    text: str
    is_correct: bool


class TestQuestion(BaseModel):
    question_text: str
    question_type: QuestionType
    correct_answer: Optional[str] = None
    options: Optional[List[QuestionOption]] = None
    explanation: Optional[str] = None
    points: int = 1


class TestResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    difficulty: Difficulty
    question_count: int
    questions: List[TestQuestion]
    created_at: datetime


class TestAttemptRequest(BaseModel):
    test_id: int
    user_id: int
    answers: dict


class TestAttemptResponse(BaseModel):
    id: int
    test_id: int
    score: int
    max_score: int
    percentage: float
    completed_at: datetime


# ============================================================================
# FLASHCARD MODELS
# ============================================================================

class FlashcardDeckCreate(BaseModel):
    class_id: Optional[int] = None
    user_id: int
    title: str
    description: Optional[str] = None


class FlashcardCreate(BaseModel):
    deck_id: int
    front_text: str
    back_text: str


class FlashcardResponse(BaseModel):
    id: int
    front_text: str
    back_text: str
    order_index: Optional[int]


class FlashcardDeckResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    card_count: int
    cards: List[FlashcardResponse]
    created_at: datetime


class FlashcardReviewRequest(BaseModel):
    card_id: int
    user_id: int
    quality: int = Field(ge=0, le=5)


class FlashcardReviewResponse(BaseModel):
    id: int
    next_review_date: datetime
    interval_days: int
    ease_factor: float
