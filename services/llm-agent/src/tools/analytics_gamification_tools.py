"""
Analytics & Gamification Tools
LangChain tools for study-analytics and gamification services
"""
from langchain_core.tools import tool
import httpx
import os
from typing import Optional

# Service URLs
ANALYTICS_SERVICE_URL = os.getenv("ANALYTICS_SERVICE_URL", "http://study-analytics-service:8012")
GAMIFICATION_SERVICE_URL = os.getenv("GAMIFICATION_SERVICE_URL", "http://gamification-service:8011")


@tool
def check_my_study_progress() -> str:
    """Check my study session history and progress.
    
    Use this tool when the user wants to see their study sessions or track their progress.
    
    Returns:
        String with formatted study session history, or error message.
    """
    try:
        response = httpx.get(
            f"{ANALYTICS_SERVICE_URL}/api/sessions",
            params={"limit": 10},
            timeout=10.0
        )
        
        if response.status_code == 200:
            data = response.json()
            sessions = data.get("sessions", [])
            
            if not sessions:
                return "No study sessions logged yet. Start studying to track your progress!"
            
            total_minutes = sum(s.get('duration_minutes', 0) for s in sessions)
            result = f"✓ Found {len(sessions)} recent study session(s)\n"
            result += f"  Total Study Time: {total_minutes} minutes ({total_minutes/60:.1f} hours)\n\n"
            
            for session in sessions[:5]:
                result += f"📚 Session {session.get('id')}\n"
                if session.get('class_id'):
                    result += f"  Class ID: {session.get('class_id')}\n"
                result += f"  Type: {session.get('session_type', 'study')}\n"
                result += f"  Duration: {session.get('duration_minutes', 0)} minutes\n"
                if session.get('mood_rating'):
                    result += f"  Mood: {session.get('mood_rating')}/5\n"
                if session.get('productivity_rating'):
                    result += f"  Productivity: {session.get('productivity_rating')}/5\n"
                result += f"  Date: {session.get('start_time', 'unknown')}\n\n"
            
            return result
            
        elif response.status_code == 401:
            return "Authentication required. This feature requires user authentication."
        else:
            return f"Error retrieving study progress: HTTP {response.status_code}"
            
    except httpx.TimeoutException:
        return "Error: Request timed out while retrieving study progress."
    except httpx.RequestError as e:
        return f"Error connecting to analytics service: {str(e)}"
    except Exception as e:
        return f"Unexpected error checking study progress: {str(e)}"


@tool
def check_my_points_and_level() -> str:
    """Check my gamification points, level, and streak.
    
    Use this tool when the user wants to see their points, level, or daily streak.
    
    Returns:
        String with formatted points and level information, or error message.
    """
    try:
        response = httpx.get(
            f"{GAMIFICATION_SERVICE_URL}/api/points",
            timeout=10.0
        )
        
        if response.status_code == 200:
            data = response.json()
            
            total_points = data.get('total_points', 0)
            level = data.get('level', 1)
            streak = data.get('streak_days', 0)
            
            result = "🏆 Your Gamification Stats\n\n"
            result += f"  Total Points: {total_points:,}\n"
            result += f"  Level: {level}\n"
            result += f"  Daily Streak: {streak} day(s) 🔥\n"
            
            if streak > 7:
                result += "\n  Amazing streak! Keep it up! 💪"
            elif streak > 0:
                result += "\n  Nice streak going! Don't break it! 🎯"
            else:
                result += "\n  Start a new streak today! 🚀"
            
            return result
            
        elif response.status_code == 401:
            return "Authentication required. This feature requires user authentication."
        else:
            return f"Error retrieving points: HTTP {response.status_code}"
            
    except httpx.TimeoutException:
        return "Error: Request timed out while retrieving points."
    except httpx.RequestError as e:
        return f"Error connecting to gamification service: {str(e)}"
    except Exception as e:
        return f"Unexpected error checking points: {str(e)}"
