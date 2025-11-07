"""
Class Management Tools
LangChain tools for interacting with class-management-service
"""
from langchain_core.tools import tool
import httpx
import os
from typing import Optional

# Service URL from environment or default to Docker service name
# Note: Within Docker network, use container internal port (8005), not host port (8006)
CLASS_SERVICE_URL = os.getenv("CLASS_SERVICE_URL", "http://class-management-service:8005")


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


@tool
def add_assignment(
    class_id: int,
    title: str,
    due_date: str,
    description: Optional[str] = None,
    assignment_type: str = "homework",
    priority: str = "medium"
) -> str:
    """Add a new assignment to a class.
    
    Use this tool when the user wants to create an assignment, add homework,
    or says something like "I have homework due Friday" or "add a test to my Physics class".
    
    Args:
        class_id: ID of the class to add assignment to (required)
        title: Title/name of the assignment (required, e.g. "Chapter 5 Homework", "Midterm Exam")
        due_date: Due date in ISO format (required, e.g. "2024-11-08T23:59:59")
        description: Detailed description of the assignment (optional)
        assignment_type: Type of assignment (optional, default "homework", can be "homework", "test", "quiz", "project", "reading")
        priority: Priority level (optional, default "medium", can be "low", "medium", "high")
    
    Returns:
        String confirming assignment creation or an error message.
    """
    try:
        payload = {
            "class_id": class_id,
            "title": title,
            "due_date": due_date,
            "type": assignment_type,
            "priority": priority,
            "status": "pending"
        }
        
        if description:
            payload["description"] = description
        
        response = httpx.post(
            f"{CLASS_SERVICE_URL}/api/assignments",
            json=payload,
            timeout=10.0
        )
        
        if response.status_code == 201:
            assignment_data = response.json()
            result = f"✓ Successfully added assignment '{assignment_data['title']}' (ID: {assignment_data['id']})"
            result += f"\n  Class ID: {assignment_data['class_id']}"
            result += f"\n  Type: {assignment_data['type']}"
            result += f"\n  Due: {assignment_data['due_date']}"
            result += f"\n  Status: {assignment_data['status']}"
            result += f"\n  Priority: {assignment_data['priority']}"
            
            if assignment_data.get('description'):
                result += f"\n  Description: {assignment_data['description']}"
            
            return result
            
        elif response.status_code == 404:
            return f"Error: Class with ID {class_id} not found. Please check the class ID."
        else:
            error_detail = response.text
            return f"Error creating assignment: HTTP {response.status_code} - {error_detail}"
            
    except httpx.TimeoutException:
        return "Error: Request timed out while creating assignment. The service may be unavailable."
    except httpx.RequestError as e:
        return f"Error connecting to class service: {str(e)}"
    except Exception as e:
        return f"Unexpected error creating assignment: {str(e)}"


@tool
def list_assignments(
    class_id: Optional[int] = None,
    status_filter: Optional[str] = None
) -> str:
    """List assignments, optionally filtered by class or status.
    
    Use this tool when the user asks to see their assignments, homework, or
    wants to know what's due. Can filter by specific class or status.
    
    Args:
        class_id: Filter by specific class ID (optional)
        status_filter: Filter by status (optional, can be "pending", "in-progress", "completed", "overdue")
    
    Returns:
        String listing assignments or an error message.
    """
    try:
        params = {}
        if class_id:
            params["class_id"] = class_id
        if status_filter:
            params["status_filter"] = status_filter
        
        response = httpx.get(
            f"{CLASS_SERVICE_URL}/api/assignments",
            params=params,
            timeout=10.0
        )
        
        if response.status_code == 200:
            assignments = response.json()
            
            if not assignments:
                msg = "You don't have any assignments"
                if class_id:
                    msg += f" for class ID {class_id}"
                if status_filter:
                    msg += f" with status '{status_filter}'"
                msg += "."
                return msg
            
            # Format assignments into readable text
            result = f"Found {len(assignments)} assignment(s)"
            if class_id:
                result += f" for class ID {class_id}"
            if status_filter:
                result += f" with status '{status_filter}'"
            result += ":\n\n"
            
            for assignment in assignments:
                status_icon = "✓" if assignment['status'] == 'completed' else "○"
                result += f"{status_icon} {assignment['title']}"
                result += f" (ID: {assignment['id']})"
                result += f"\n  Type: {assignment['type']}"
                result += f"\n  Due: {assignment['due_date']}"
                result += f"\n  Status: {assignment['status']}"
                result += f"\n  Priority: {assignment['priority']}"
                
                if assignment.get('description'):
                    result += f"\n  Description: {assignment['description'][:100]}"
                    if len(assignment.get('description', '')) > 100:
                        result += "..."
                result += "\n\n"
            
            return result
        else:
            return f"Error fetching assignments: HTTP {response.status_code}"
            
    except httpx.TimeoutException:
        return "Error: Request timed out while fetching assignments. The service may be unavailable."
    except httpx.RequestError as e:
        return f"Error connecting to class service: {str(e)}"
    except Exception as e:
        return f"Unexpected error listing assignments: {str(e)}"


@tool
def update_assignment_status(
    assignment_id: int,
    new_status: str
) -> str:
    """Update the status of an assignment.
    
    Use this tool when the user wants to mark an assignment as complete,
    in progress, or change its status.
    
    Args:
        assignment_id: ID of the assignment to update (required)
        new_status: New status (required, must be one of: "pending", "in-progress", "completed", "overdue")
    
    Returns:
        String confirming status update or an error message.
    """
    # Validate status
    valid_statuses = ["pending", "in-progress", "completed", "overdue"]
    if new_status not in valid_statuses:
        return f"Error: Invalid status '{new_status}'. Must be one of: {', '.join(valid_statuses)}"
    
    try:
        response = httpx.patch(
            f"{CLASS_SERVICE_URL}/api/assignments/{assignment_id}/status",
            params={"new_status": new_status},
            timeout=10.0
        )
        
        if response.status_code == 200:
            assignment_data = response.json()
            result = f"✓ Successfully updated assignment '{assignment_data['title']}'"
            result += f"\n  Status: {assignment_data['status']}"
            result += f"\n  Due: {assignment_data['due_date']}"
            
            if new_status == "completed":
                result += "\n\nGreat job completing this assignment! 🎉"
            
            return result
            
        elif response.status_code == 404:
            return f"Error: Assignment with ID {assignment_id} not found."
        else:
            error_detail = response.text
            return f"Error updating assignment status: HTTP {response.status_code} - {error_detail}"
            
    except httpx.TimeoutException:
        return "Error: Request timed out while updating assignment. The service may be unavailable."
    except httpx.RequestError as e:
        return f"Error connecting to class service: {str(e)}"
    except Exception as e:
        return f"Unexpected error updating assignment: {str(e)}"
