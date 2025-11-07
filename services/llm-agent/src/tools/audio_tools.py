"""
Audio Tools
LangChain tools for speech-to-text and text-to-speech services
"""
from langchain_core.tools import tool
import httpx
import os
from typing import Optional

# Service URLs
STT_SERVICE_URL = os.getenv("STT_SERVICE_URL", "http://stt-service:8002")
TTS_SERVICE_URL = os.getenv("TTS_SERVICE_URL", "http://tts-service:8003")


@tool
def list_my_transcriptions(class_id: Optional[int] = None, limit: int = 10) -> str:
    """List my audio transcriptions (speech-to-text results).
    
    Use this tool when the user wants to see their transcribed audio recordings.
    
    Args:
        class_id: Optional class ID to filter transcriptions
        limit: Maximum number of transcriptions to return (default: 10, max: 50)
    
    Returns:
        String with formatted list of transcriptions, or error message.
    """
    try:
        params = {"limit": min(limit, 50)}
        if class_id:
            params["class_id"] = class_id
        
        response = httpx.get(
            f"{STT_SERVICE_URL}/api/transcriptions",
            params=params,
            timeout=10.0
        )
        
        if response.status_code == 200:
            transcriptions = response.json()
            
            if not transcriptions:
                return "No transcriptions found. Record and transcribe audio to see them here!"
            
            result = f"✓ Found {len(transcriptions)} transcription(s):\n\n"
            
            for trans in transcriptions:
                result += f"🎤 Transcription ID: {trans.get('id')}\n"
                if trans.get('class_id'):
                    result += f"  Class ID: {trans.get('class_id')}\n"
                result += f"  Duration: {trans.get('duration_seconds', 0)} seconds\n"
                result += f"  Status: {trans.get('status', 'unknown')}\n"
                
                if trans.get('transcript_text'):
                    text_preview = trans['transcript_text'][:150]
                    if len(trans['transcript_text']) > 150:
                        text_preview += "..."
                    result += f"  Text: {text_preview}\n"
                    
                result += f"  Created: {trans.get('created_at', 'unknown')}\n\n"
            
            return result
            
        elif response.status_code == 401:
            return "Authentication required. This feature requires user authentication."
        elif response.status_code == 404:
            return "Transcription service endpoint not found. The service may not be running."
        else:
            return f"Error retrieving transcriptions: HTTP {response.status_code}"
            
    except httpx.TimeoutException:
        return "Error: Request timed out while retrieving transcriptions."
    except httpx.RequestError as e:
        return f"Error connecting to speech-to-text service: {str(e)}"
    except Exception as e:
        return f"Unexpected error listing transcriptions: {str(e)}"
