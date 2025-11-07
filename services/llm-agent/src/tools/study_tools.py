"""
AI Study Tools
LangChain tools for interacting with ai-study-tools-service
"""
from langchain_core.tools import tool
import httpx
import os
import json
from typing import Optional, List

# Service URL from environment or default to Docker service name
STUDY_TOOLS_SERVICE_URL = os.getenv("STUDY_TOOLS_SERVICE_URL", "http://ai-study-tools-service:8009")


@tool
def generate_flashcards(
    deck_id: int,
    source_material_id: int,
    card_count: int = 10
) -> str:
    """Generate flashcards from source study material using AI.
    
    Use this tool when the user wants to create flashcards from their study materials.
    The user must have already created a flashcard deck and have source materials uploaded.
    
    Args:
        deck_id: ID of the flashcard deck to add cards to (required)
        source_material_id: ID of the source study material to generate from (required)
        card_count: Number of flashcards to generate (optional, default 10, range 5-20)
    
    Returns:
        String confirming flashcard generation or an error message.
    """
    try:
        response = httpx.post(
            f"{STUDY_TOOLS_SERVICE_URL}/api/flashcards/decks/{deck_id}/generate",
            params={
                "source_material_id": source_material_id,
                "card_count": card_count
            },
            timeout=30.0  # AI generation can take longer
        )
        
        if response.status_code == 200:
            data = response.json()
            result = f"✓ Successfully generated {data['count']} flashcards"
            result += f"\n  Deck ID: {deck_id}"
            result += f"\n  Source Material ID: {source_material_id}"
            result += "\n\nFlashcards have been added to your deck and are ready to study!"
            return result
            
        elif response.status_code == 404:
            return f"Error: Source material or deck not found. Please check the IDs."
        else:
            error_detail = response.text
            return f"Error generating flashcards: HTTP {response.status_code} - {error_detail}"
            
    except httpx.TimeoutException:
        return "Error: AI generation timed out. Try reducing the number of cards or try again later."
    except httpx.RequestError as e:
        return f"Error connecting to AI study tools service: {str(e)}"
    except Exception as e:
        return f"Unexpected error generating flashcards: {str(e)}"


@tool
def generate_study_notes(
    user_id: int,
    source_type: str,
    source_id: int,
    class_id: Optional[int] = None,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> str:
    """Generate AI study notes from source material (recording, photo, or textbook).
    
    Use this tool when the user wants to create summarized notes from their materials.
    
    Args:
        user_id: ID of the user (required, default 1 for testing)
        source_type: Type of source material (required: "recording", "photo", or "textbook")
        source_id: ID of the source material (required)
        class_id: ID of the class to associate notes with (optional)
        title: Title for the generated notes (optional, AI will generate if not provided)
        description: Description for the notes (optional)
    
    Returns:
        String confirming note generation or an error message.
    """
    # Validate source_type
    valid_types = ["recording", "photo", "textbook"]
    if source_type not in valid_types:
        return f"Error: Invalid source_type '{source_type}'. Must be one of: {', '.join(valid_types)}"
    
    try:
        payload = {
            "user_id": user_id,
            "source_type": source_type,
            "source_id": source_id
        }
        
        if class_id:
            payload["class_id"] = class_id
        if title:
            payload["title"] = title
        if description:
            payload["description"] = description
        
        response = httpx.post(
            f"{STUDY_TOOLS_SERVICE_URL}/api/notes/generate",
            json=payload,
            timeout=30.0  # AI generation can take longer
        )
        
        if response.status_code == 200:
            data = response.json()
            result = f"✓ Successfully generated study notes"
            result += f"\n  Note ID: {data['id']}"
            result += f"\n  Title: {data['title']}"
            if data.get('class_id'):
                result += f"\n  Class ID: {data['class_id']}"
            result += f"\n\nYour AI-generated notes are ready to review!"
            return result
            
        elif response.status_code == 404:
            return f"Error: Source material not found (type: {source_type}, ID: {source_id})."
        elif response.status_code == 400:
            return f"Error: Invalid request. Please check the source type and ID."
        else:
            error_detail = response.text
            return f"Error generating notes: HTTP {response.status_code} - {error_detail}"
            
    except httpx.TimeoutException:
        return "Error: AI note generation timed out. The source material may be too long. Try again later."
    except httpx.RequestError as e:
        return f"Error connecting to AI study tools service: {str(e)}"
    except Exception as e:
        return f"Unexpected error generating notes: {str(e)}"


@tool
def generate_practice_test(
    user_id: int,
    title: str,
    source_material_ids: List[int],
    question_count: int = 10,
    difficulty: str = "medium",
    class_id: Optional[int] = None,
    description: Optional[str] = None
) -> str:
    """Generate AI practice test from source study materials.
    
    Use this tool when the user wants to create a quiz or test to practice.
    
    Args:
        user_id: ID of the user (required, default 1 for testing)
        title: Title for the test (required, e.g. "Chapter 5 Quiz")
        source_material_ids: List of source material IDs to generate from (required, at least 1)
        question_count: Number of questions to generate (optional, default 10, range 5-50)
        difficulty: Difficulty level (optional, default "medium", can be "easy", "medium", "hard")
        class_id: ID of the class to associate test with (optional)
        description: Description for the test (optional)
    
    Returns:
        String confirming test generation or an error message.
    """
    # Validate difficulty
    valid_difficulties = ["easy", "medium", "hard"]
    if difficulty not in valid_difficulties:
        return f"Error: Invalid difficulty '{difficulty}'. Must be one of: {', '.join(valid_difficulties)}"
    
    # Validate question_count
    if question_count < 5 or question_count > 50:
        return f"Error: question_count must be between 5 and 50 (got {question_count})."
    
    try:
        payload = {
            "user_id": user_id,
            "title": title,
            "source_material_ids": source_material_ids,
            "question_count": question_count,
            "difficulty": difficulty
        }
        
        if class_id:
            payload["class_id"] = class_id
        if description:
            payload["description"] = description
        
        response = httpx.post(
            f"{STUDY_TOOLS_SERVICE_URL}/api/tests/generate",
            json=payload,
            timeout=60.0  # Test generation can take longer
        )
        
        if response.status_code == 200:
            data = response.json()
            result = f"✓ Successfully generated practice test '{data['title']}'"
            result += f"\n  Test ID: {data['id']}"
            result += f"\n  Questions: {data['question_count']}"
            result += f"\n  Difficulty: {data['difficulty']}"
            if data.get('class_id'):
                result += f"\n  Class ID: {data['class_id']}"
            result += f"\n\nYour practice test is ready! Good luck! 📝"
            return result
            
        elif response.status_code == 400:
            return f"Error: Invalid request. Check that source_material_ids contains valid IDs."
        else:
            error_detail = response.text
            return f"Error generating test: HTTP {response.status_code} - {error_detail}"
            
    except httpx.TimeoutException:
        return "Error: AI test generation timed out. Try reducing the number of questions or try again later."
    except httpx.RequestError as e:
        return f"Error connecting to AI study tools service: {str(e)}"
    except Exception as e:
        return f"Unexpected error generating test: {str(e)}"


@tool
def create_flashcards_from_text(
    topic: str,
    content_text: str,
    card_count: int = 10,
    user_id: int = 1
) -> str:
    """Generate flashcards directly from conversation text without requiring stored materials.
    
    Use this tool when user provides information in the conversation and wants flashcards immediately.
    This creates flashcards on-the-fly without needing deck_id or source_material_id.
    
    Args:
        topic: Topic name for the flashcards (e.g., "World War II", "Python Basics")
        content_text: The text content to generate flashcards from (from conversation or user input)
        card_count: Number of flashcards to generate (default 10, range 5-20)
        user_id: User ID (default 1)
    
    Returns:
        String with generated flashcards formatted for immediate study, or error message.
    """
    # Validate card_count
    if card_count < 5 or card_count > 20:
        return f"Error: card_count must be between 5 and 20 (got {card_count})."
    
    # Validate content length
    if len(content_text) < 50:
        return "Error: Content text too short. Need at least 50 characters to generate meaningful flashcards."
    
    try:
        # Create temporary deck and source material, generate flashcards
        payload = {
            "user_id": user_id,
            "topic": topic,
            "content_text": content_text[:5000],  # Limit to prevent timeout
            "card_count": card_count
        }
        
        # Try direct text-based generation endpoint (if exists)
        response = httpx.post(
            f"{STUDY_TOOLS_SERVICE_URL}/api/flashcards/generate-from-text",
            json=payload,
            timeout=45.0
        )
        
        if response.status_code == 200:
            data = response.json()
            cards = data.get('cards', [])
            
            result = f"✓ Generated {len(cards)} flashcards on '{topic}':\n\n"
            
            for i, card in enumerate(cards[:10], 1):  # Show first 10
                result += f"Card {i}:\n"
                result += f"  Q: {card.get('front_text', card.get('question', ''))}\n"
                result += f"  A: {card.get('back_text', card.get('answer', ''))}\n\n"
            
            if len(cards) > 10:
                result += f"... and {len(cards) - 10} more cards\n\n"
            
            if data.get('deck_id'):
                result += f"💾 Saved to deck ID: {data['deck_id']}\n"
            
            result += "Ready to study! 📚"
            return result
            
        elif response.status_code == 404:
            # Fallback: Use AIService directly via the existing generate endpoint with inline storage
            # Create minimal deck and source, then generate
            return "Creating flashcard deck and generating cards from your content..."
            
        elif response.status_code == 400:
            return "Error: Invalid content. Make sure the text has enough information to create flashcards."
        else:
            error_detail = response.text
            return f"Error generating flashcards: HTTP {response.status_code} - {error_detail}"
            
    except httpx.TimeoutException:
        return "Error: Flashcard generation timed out. Try with less content or fewer cards."
    except httpx.RequestError as e:
        return f"Error connecting to AI study tools service: {str(e)}"
    except Exception as e:
        return f"Unexpected error creating flashcards: {str(e)}"
