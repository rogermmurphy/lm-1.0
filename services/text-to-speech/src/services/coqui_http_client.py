"""
Text-to-Speech Service - Coqui TTS HTTP Client
Connects to Coqui TTS Docker container via HTTP API
"""
import requests
from ..config import settings


class CoquiHTTPClient:
    """HTTP client for Coqui TTS server"""
    
    def __init__(self):
        """Initialize with Coqui server URL"""
        self.base_url = settings.COQUI_TTS_URL
        self.enabled = settings.ENABLE_COQUI
    
    def is_available(self) -> bool:
        """Check if Coqui server is available"""
        if not self.enabled:
            return False
        try:
            response = requests.get(f"{self.base_url}/api/tts", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def synthesize(self, text: str, output_file: str) -> bool:
        """
        Convert text to speech using Coqui TTS HTTP API
        
        Args:
            text: Text to convert
            output_file: Output file path
            
        Returns:
            True if successful
        """
        if not self.enabled:
            print("Coqui TTS is disabled")
            return False
        
        try:
            # Call Coqui TTS server API
            response = requests.get(
                f"{self.base_url}/api/tts",
                params={"text": text},
                timeout=120  # Coqui is slow, give it time
            )
            
            if response.status_code == 200:
                # Write audio to file
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"Coqui TTS error: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            print("Coqui TTS request timed out (>120s)")
            return False
        except Exception as e:
            print(f"Coqui TTS request failed: {e}")
            return False
