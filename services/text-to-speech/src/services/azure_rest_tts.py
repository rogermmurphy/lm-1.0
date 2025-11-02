"""
Text-to-Speech Service - Azure REST API Implementation
Using direct HTTP calls to Azure TTS REST API (no SDK needed!)
"""
import requests
from ..config import settings


class AzureRestTTSService:
    """Azure Text-to-Speech using REST API directly"""
    
    def __init__(self):
        """Initialize with Azure credentials"""
        if not settings.AZURE_SPEECH_KEY:
            raise ValueError("AZURE_SPEECH_KEY required")
        
        self.api_key = settings.AZURE_SPEECH_KEY
        self.region = settings.AZURE_SPEECH_REGION
        self.endpoint = f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"
    
    def synthesize(self, text: str, output_file: str, voice: str = None) -> bool:
        """
        Convert text to speech using Azure REST API
        
        Args:
            text: Text to convert
            output_file: Output file path
            voice: Voice name (default from settings)
            
        Returns:
            True if successful
        """
        voice_name = voice or settings.DEFAULT_VOICE
        
        # Build SSML
        ssml = f"""
        <speak version='1.0' xml:lang='en-US'>
            <voice xml:lang='en-US' name='{voice_name}'>
                {text}
            </voice>
        </speak>
        """
        
        # Set headers
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'LittleMonsterTTS'
        }
        
        try:
            # Make HTTP POST request
            response = requests.post(
                self.endpoint,
                headers=headers,
                data=ssml.encode('utf-8'),
                timeout=30
            )
            
            if response.status_code == 200:
                # Write audio to file
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"Azure TTS error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Azure TTS request failed: {e}")
            return False
