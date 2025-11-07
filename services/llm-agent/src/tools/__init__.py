"""
LangChain Tools for Service API Integration
Tool-based AI assistant that can execute application features
"""

from .class_tools import (
    list_user_classes,
    create_class_tool,
    add_assignment,
    list_assignments,
    update_assignment_status
)
from .study_tools import (
    generate_flashcards,
    generate_study_notes,
    generate_practice_test,
    create_flashcards_from_text
)
from .content_tools import (
    list_my_photos,
    list_my_textbooks
)
from .social_tools import (
    create_study_group,
    list_my_study_groups,
    list_my_connections
)
from .analytics_gamification_tools import (
    check_my_study_progress,
    check_my_points_and_level
)
from .audio_tools import (
    list_my_transcriptions
)
from .web_research_tools import (
    search_web,
    fetch_url,
    get_documentation
)

__all__ = [
    # Class Management
    "list_user_classes",
    "create_class_tool",
    "add_assignment",
    "list_assignments",
    "update_assignment_status",
    # AI Study Tools
    "generate_flashcards",
    "generate_study_notes",
    "generate_practice_test",
    "create_flashcards_from_text",
    # Content Capture Tools
    "list_my_photos",
    "list_my_textbooks",
    # Social Collaboration Tools
    "create_study_group",
    "list_my_study_groups",
    "list_my_connections",
    # Analytics & Gamification Tools
    "check_my_study_progress",
    "check_my_points_and_level",
    # Audio Tools
    "list_my_transcriptions",
    # Web Research Tools
    "search_web",
    "fetch_url",
    "get_documentation",
]
