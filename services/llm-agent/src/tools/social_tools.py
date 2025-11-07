"""
Social Collaboration Tools
LangChain tools for interacting with social-collaboration-service
"""
from langchain_core.tools import tool
import httpx
import os
from typing import Optional

# Service URL from environment or default to Docker service name
SOCIAL_SERVICE_URL = os.getenv("SOCIAL_SERVICE_URL", "http://social-collaboration-service:8010")


@tool
def create_study_group(
    name: str,
    description: Optional[str] = None,
    class_id: Optional[int] = None,
    max_members: int = 10
) -> str:
    """Create a new study group for collaboration.
    
    Use this tool when the user wants to create a study group to collaborate with classmates.
    
    Args:
        name: Name of the study group (required, e.g. "Physics 101 Study Group")
        description: Optional description of the group's purpose
        class_id: Optional class ID to associate with the group
        max_members: Maximum number of members (default: 10, range: 2-50)
    
    Returns:
        String confirming group creation or an error message.
    """
    # Validate max_members
    if max_members < 2 or max_members > 50:
        return f"Error: max_members must be between 2 and 50 (got {max_members})."
    
    try:
        payload = {
            "name": name,
            "description": description,
            "class_id": class_id,
            "max_members": max_members
        }
        
        response = httpx.post(
            f"{SOCIAL_SERVICE_URL}/api/groups/",
            json=payload,
            timeout=10.0
        )
        
        if response.status_code == 200:
            data = response.json()
            group = data.get('group', {})
            result = f"✓ Study group '{group.get('name')}' created successfully"
            result += f"\n  Group ID: {group.get('id')}"
            if group.get('class_id'):
                result += f"\n  Class ID: {group.get('class_id')}"
            result += f"\n  Max Members: {group.get('max_members')}"
            result += f"\n  Status: Active"
            result += "\n\nYou are the admin of this group. Invite classmates to join! 👥"
            return result
            
        elif response.status_code == 400:
            return f"Error: Invalid group data. Please check the name and parameters."
        elif response.status_code == 401:
            return "Authentication required. This feature requires user authentication."
        else:
            return f"Error creating study group: HTTP {response.status_code} - {response.text}"
            
    except httpx.TimeoutException:
        return "Error: Request timed out while creating study group."
    except httpx.RequestError as e:
        return f"Error connecting to social collaboration service: {str(e)}"
    except Exception as e:
        return f"Unexpected error creating study group: {str(e)}"


@tool
def list_my_study_groups() -> str:
    """List all study groups I'm a member of.
    
    Use this tool when the user wants to see their study groups.
    
    Returns:
        String with formatted list of study groups and membership details, or error message.
    """
    try:
        response = httpx.get(
            f"{SOCIAL_SERVICE_URL}/api/groups/my-groups",
            timeout=10.0
        )
        
        if response.status_code == 200:
            groups = response.json()
            
            if not groups:
                return "You're not a member of any study groups yet. Create one to get started!"
            
            result = f"✓ You're a member of {len(groups)} study group(s):\n\n"
            
            for group in groups:
                result += f"👥 {group.get('name')}\n"
                result += f"  Group ID: {group.get('id')}\n"
                if group.get('description'):
                    result += f"  Description: {group.get('description')}\n"
                if group.get('class_id'):
                    result += f"  Class ID: {group.get('class_id')}\n"
                result += f"  Your Role: {group.get('role', 'member')}\n"
                result += f"  Max Members: {group.get('max_members', 'unlimited')}\n"
                result += f"  Joined: {group.get('joined_at', 'unknown')}\n\n"
            
            return result
            
        elif response.status_code == 401:
            return "Authentication required. This feature requires user authentication."
        elif response.status_code == 404:
            return "Study groups endpoint not found. The service may not be running."
        else:
            return f"Error retrieving study groups: HTTP {response.status_code} - {response.text}"
            
    except httpx.TimeoutException:
        return "Error: Request timed out while retrieving study groups."
    except httpx.RequestError as e:
        return f"Error connecting to social collaboration service: {str(e)}"
    except Exception as e:
        return f"Unexpected error listing study groups: {str(e)}"


@tool
def list_my_connections(status: Optional[str] = None) -> str:
    """List classmate connections (friends/study partners).
    
    Use this tool when the user wants to see their connections with other students.
    
    Args:
        status: Optional filter by connection status:
                "accepted" = confirmed connections
                "pending" = pending requests  
                "blocked" = blocked users
                None = all connections
    
    Returns:
        String with formatted list of connections, or error message.
    """
    # Validate status if provided
    valid_statuses = ["accepted", "pending", "blocked"]
    if status and status not in valid_statuses:
        return f"Error: Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)} or None."
    
    try:
        params = {}
        if status:
            params["status"] = status
        
        response = httpx.get(
            f"{SOCIAL_SERVICE_URL}/api/connections",
            params=params,
            timeout=10.0
        )
        
        if response.status_code == 200:
            connections = response.json()
            
            if not connections:
                status_msg = f" with status '{status}'" if status else ""
                return f"No connections found{status_msg}. Send connection requests to build your network!"
            
            result = f"✓ Found {len(connections)} connection(s)"
            if status:
                result += f" (status: {status})"
            result += ":\n\n"
            
            for conn in connections:
                status_emoji = {"accepted": "✓", "pending": "⏳", "blocked": "🚫"}.get(conn.get('status', ''), "•")
                result += f"{status_emoji} Connection ID: {conn.get('id')}\n"
                result += f"  Classmate User ID: {conn.get('classmate_user_id')}\n"
                result += f"  Status: {conn.get('status')}\n"
                result += f"  Created: {conn.get('created_at', 'unknown')}\n\n"
            
            return result
            
        elif response.status_code == 401:
            return "Authentication required. This feature requires user authentication."
        elif response.status_code == 404:
            return "Connections endpoint not found. The service may not be running."
        else:
            return f"Error retrieving connections: HTTP {response.status_code} - {response.text}"
            
    except httpx.TimeoutException:
        return "Error: Request timed out while retrieving connections."
    except httpx.RequestError as e:
        return f"Error connecting to social collaboration service: {str(e)}"
    except Exception as e:
        return f"Unexpected error listing connections: {str(e)}"
