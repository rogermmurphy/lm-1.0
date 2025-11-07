"""
Agent Service
Tool-using AI assistant with Bedrock Claude
Uses native tool calling instead of LangChain agents for compatibility
"""
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import List, Dict, Any
import os
import json

from ..tools import (
    list_user_classes,
    create_class_tool,
    add_assignment,
    list_assignments,
    update_assignment_status,
    generate_flashcards,
    generate_study_notes,
    generate_practice_test,
    create_flashcards_from_text,
    list_my_photos,
    list_my_textbooks,
    create_study_group,
    list_my_study_groups,
    list_my_connections,
    check_my_study_progress,
    check_my_points_and_level,
    list_my_transcriptions,
    search_web,
    fetch_url,
    get_documentation
)
from .rag_service import RAGService
from lm_common.logging import get_logger
from datetime import datetime

logger = get_logger(__name__)


# System prompt with dynamic date/time
def get_system_prompt() -> str:
    """Generate system prompt with current date/time"""
    current_datetime = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    
    return f"""You are Little Monster's AI assistant. You help students manage their classes, assignments, and study materials.

**Current Date and Time:** {current_datetime}


You have access to these tools that can execute actions:

CLASS MANAGEMENT:
- list_user_classes: List all classes for the current user
- create_class_tool: Create a new class (requires: name, optional: teacher_name, period, subject, color)

ASSIGNMENT MANAGEMENT:
- add_assignment: Add an assignment to a class (requires: class_id, title, due_date, optional: description, assignment_type, priority)
- list_assignments: List assignments, optionally filtered by class_id or status
- update_assignment_status: Update assignment status (requires: assignment_id, new_status: "pending"|"in-progress"|"completed"|"overdue")

AI STUDY TOOLS:
- generate_flashcards: Generate flashcards from stored study material (requires: deck_id, source_material_id, optional: card_count)
- create_flashcards_from_text: Generate flashcards from conversation text immediately (requires: topic, content_text, optional: card_count) - USE THIS when user provides info in chat
- generate_study_notes: Generate AI notes from recordings/photos/textbooks (requires: user_id, source_type, source_id, optional: class_id, title)
- generate_practice_test: Generate practice test from materials (requires: user_id, title, source_material_ids, optional: question_count, difficulty, class_id)

CONTENT CAPTURE:
- list_my_photos: List uploaded photos with OCR text (optional: class_id, limit)
- list_my_textbooks: List uploaded textbook PDFs and processing status (optional: class_id, limit)

WHEN TO USE TOOLS:
- User asks about their classes → use list_user_classes
- User wants to create a class → use create_class_tool
- User mentions homework, assignments, or due dates → use add_assignment or list_assignments
- User wants to mark something complete → use update_assignment_status
- User wants flashcards from stored material → use generate_flashcards
- User provides info in chat and wants flashcards → use create_flashcards_from_text
- User wants summarized notes → use generate_study_notes
- User wants a practice test/quiz → use generate_practice_test
- User asks about their photos → use list_my_photos
- User asks about their textbooks → use list_my_textbooks
- User wants to create a study group → use create_study_group
- User asks about their study groups → use list_my_study_groups
- User asks about connections/classmates → use list_my_connections
- User asks about their study progress/sessions → use check_my_study_progress
- User asks about points/level/streak → use check_my_points_and_level
- User asks about transcriptions/audio → use list_my_transcriptions

WEB RESEARCH TOOLS:
- search_web: Search the web for current information, news, or topics not in your training data
- fetch_url: Get full content from a specific URL
- get_documentation: Get up-to-date library/framework documentation (e.g., React, Python libraries)

WHEN TO USE WEB RESEARCH:
- User asks about current events, recent news, or breaking information
- User asks "what's happening with [topic]" or "latest news about [topic]"
- User asks about topics/technologies you don't have training data for
- User wants to know "what is [new technology/concept]"
- User asks for documentation on libraries/frameworks
- User provides a URL and wants you to read it

MULTI-STEP WORKFLOWS:
If user says "create Physics 101 and add homework due Friday":
1. First call create_class_tool to get the class_id
2. Then call add_assignment with that class_id

For general questions, answer directly using your knowledge. If you don't have current information, use web research tools.
Always be helpful, clear, and encouraging."""


SYSTEM_PROMPT = get_system_prompt()


class AgentService:
    """Tool-using AI service with Bedrock Claude"""
    
    def __init__(self):
        """Initialize service with Bedrock Claude and tools"""
        logger.info("Initializing AgentService...")
        
        # Get AWS credentials from environment
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        bedrock_model = os.getenv("BEDROCK_MODEL", "anthropic.claude-3-sonnet-20240229-v1:0")
        
        if not aws_access_key or not aws_secret_key:
            raise ValueError("AWS credentials not found in environment")
        
        # Initialize Bedrock LLM with tool binding
        # Optimized parameters for better memory and coherence
        logger.info(f"Connecting to AWS Bedrock ({bedrock_model})...")
        self.llm = ChatBedrock(
            model_id=bedrock_model,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region,
            model_kwargs={
                "temperature": 0.3,      # Lower for more consistent, focused responses
                "max_tokens": 4096,      # Higher for complex multi-step responses
                "top_p": 0.95,           # Slightly higher for better coherence
                "top_k": 250             # Add top_k for more deterministic output
            }
        )
        
        # Initialize tools
        self.tools = [
            # Class Management
            list_user_classes,
            create_class_tool,
            add_assignment,
            list_assignments,
            update_assignment_status,
            # AI Study Tools
            generate_flashcards,
            generate_study_notes,
            generate_practice_test,
            create_flashcards_from_text,
            # Content Capture
            list_my_photos,
            list_my_textbooks,
            # Social Collaboration
            create_study_group,
            list_my_study_groups,
            list_my_connections,
            # Analytics & Gamification
            check_my_study_progress,
            check_my_points_and_level,
            # Audio
            list_my_transcriptions,
            # Web Research
            search_web,
            fetch_url,
            get_documentation,
        ]
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Initialize RAG service for context
        self.rag_service = RAGService()
        
        logger.info("AgentService initialized successfully with tool binding")
    
    def chat(
        self,
        message: str,
        conversation_history: List[Dict[str, str]] = None,
        use_rag: bool = True
    ) -> str:
        """
        Process user message with tool calling
        
        Args:
            message: User message
            conversation_history: Previous conversation messages
            use_rag: Whether to use RAG context (default: True)
        
        Returns:
            Assistant response string
        """
        try:
            logger.info(f"Processing message: {message[:100]}...")
            
            # Get RAG context if enabled
            context = ""
            if use_rag:
                try:
                    context, sources = self.rag_service.get_context_for_query(message, n_results=3)
                    if context:
                        logger.info(f"Retrieved RAG context from {len(sources)} sources")
                        message = f"{message}\n\n[Context from study materials: {context[:500]}...]"
                except Exception as e:
                    logger.warning(f"RAG retrieval failed: {e}")
            
            # Build messages with full conversation history
            # Get fresh system prompt with current date/time
            current_system_prompt = get_system_prompt()
            messages = [SystemMessage(content=current_system_prompt)]
            
            # Add conversation history if provided
            if conversation_history and len(conversation_history) > 0:
                logger.info(f"Including {len(conversation_history)} previous messages")
                for msg in conversation_history:
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    
                    if role == 'user':
                        messages.append(HumanMessage(content=content))
                    elif role == 'assistant':
                        messages.append(AIMessage(content=content))
            
            # Add current message
            messages.append(HumanMessage(content=message))
            
            # Invoke LLM with tools
            logger.info("Invoking LLM with tool binding...")
            response = self.llm_with_tools.invoke(messages)
            
            # Check if tool calls were made
            if hasattr(response, 'tool_calls') and response.tool_calls:
                logger.info(f"Tool calls detected: {len(response.tool_calls)}")
                
                # Execute tool calls
                tool_results = []
                for tool_call in response.tool_calls:
                    tool_name = tool_call.get('name')
                    tool_args = tool_call.get('args', {})
                    
                    logger.info(f"Executing tool: {tool_name}")
                    
                    # Find and execute tool
                    for tool in self.tools:
                        if tool.name == tool_name:
                            try:
                                result = tool.invoke(tool_args)
                                tool_results.append(result)
                            except Exception as e:
                                tool_results.append(f"Error executing {tool_name}: {str(e)}")
                            break
                
                # If we executed tools, return their results
                if tool_results:
                    return "\n\n".join(tool_results)
            
            # Return text response
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
            
        except Exception as e:
            logger.error(f"Error in agent chat: {str(e)}", exc_info=True)
            return f"I encountered an error processing your request: {str(e)}\n\nPlease try again or rephrase your question."
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return [tool.name for tool in self.tools]
