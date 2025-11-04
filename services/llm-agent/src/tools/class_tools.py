"""
Class Management Tools
LangChain tools for interacting with class-management-service
"""
from langchain_core.tools import tool
import httpx
import os
from typing import Optional

# Service URL from environment or default to Docker service name
CLASS_SERVICE_URL = os.getenv("CLASS_SERVICE_URL", "http://class-management-service:8006")


@tool
def list_user_classes() -> str:
    """List all classes for the current user.
    
    Use this tool when the user asks to see their classes, show their classes,
    or asks "what classes do I have".
    
    Returns:
        String describing the user's classes or an error message.
    """
    try:
        response = httpx.get(
            f"{CLASS_SERVICE_URL}/api/classes",
            timeout=10.0
        )
        
        if response.status_code == 200:
            classes = response.json()
            
            if not classes:
                return "You don't have any classes yet. Would you like me to create one?"
            
            # Format classes into readable text
            result = f"You have {len(classes)} class(es):\n\n"
            for cls in classes:
                result += f"• {cls['name']}"
                if cls.get('teacher_name'):
                    result += f" (Teacher: {cls['teacher_name']})"
                if cls.get('period'):
                    result += f" - Period {cls['period']}"
                if cls.get('current_grade'):
                    result += f" - Grade: {cls['current_grade']}"
                result += f" (ID: {cls['id']})\n"
            
            return result
        else:
            return f"Error fetching classes: HTTP {response.status_code}"
            
    except httpx.TimeoutException:
        return "Error: Request timed out while fetching classes. The service may be unavailable."
    except httpx.RequestError as e:
        return f"Error connecting to class service: {str(e)}"
    except Exception as e:
        return f"Unexpected error listing classes: {str(e)}"


@tool
def create_class_tool(
    name: str,
    teacher_name: Optional[str] = None,
    period: Optional[str] = None,
    subject: Optional[str] = None,
    color: Optional[str] = None
) -> str:
    """Create a new class for the user.
    
    Use this tool when the user wants to create a new class, add a class,
    or says something like "create a class called Physics 101".
    
    Args:
        name: The name of the class (required, e.g. "Physics 101", "Math Advanced")
        teacher_name: Name of the teacher (optional, e.g. "Mr. Smith")
        period: Class period (optional, e.g. "1", "2", "A")
        subject: Subject area (optional, e.g. "Science", "Math", "English")
        color: Color code for the class (optional, e.g. "#FF5733")
    
    Returns:
        String confirming class creation or an error message.
    """
    try:
        # Build request payload
        payload = {"name": name}
        
        if teacher_name:
            payload["teacher_name"] = teacher_name
        if period:
            payload["period"] = period
        if subject:
            payload["subject"] = subject
        if color:
            payload["color"] = color
        
        response = httpx.post(
            f"{CLASS_SERVICE_URL}/api/classes",
            json=payload,
            timeout=10.0
        )
        
        if response.status_code == 201:
            class_data = response.json()
            result = f"✓ Successfully created class '{class_data['name']}' (ID: {class_data['id']})"
            
            if class_data.get('teacher_name'):
                result += f"\n  Teacher: {class_data['teacher_name']}"
            if class_data.get('period'):
                result += f"\n  Period: {class_data['period']}"
            if class_data.get('subject'):
                result += f"\n  Subject: {class_data['subject']}"
            
            result += "\n\nWould you like to add any assignments to this class?"
            return result
            
        elif response.status_code == 409:
            return f"Error: A class with the name '{name}' already exists. Please choose a different name."
        else:
            return f"Error creating class: HTTP {response.status_code} - {response.text}"
            
    except httpx.TimeoutException:
        return "Error: Request timed out while creating class. The service may be unavailable."
    except httpx.RequestError as e:
        return f"Error connecting to class service: {str(e)}"
    except Exception as e:
        return f"Unexpected error creating class: {str(e)}"
