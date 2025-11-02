"""
Text-to-Speech Service - Coqui TTS Service
Using Coqui TTS which works reliably in Docker containers
"""
from TTS.api import TTS
from ..config import settings


class CoquiTTSService:
    """Coqui Text-to-Speech service - Docker-compatible"""
    
    def __init__(self):
        """Initialize Coqui TTS with Jenny voice model"""
        # Use Jenny voice model (Little Monster spec)
        self.model_name = "tts_models/en/jenny/jenny"
        self.tts = None
    
    def _ensure_initialized(self):
        """Lazy load TTS model (downloads on first use)"""
        if self.tts is None:
            self.tts = TTS(model_name=self.model_name, progress_bar=False, gpu=False)
    
    def synthesize(self, text: str, output_file: str, voice: str = None) -> bool:
        """
        Convert text to speech using Coqui TTS
        
        Args:
            text: Text to convert
            output_file: Output file path
            voice: Not used for Coqui (single Jenny model)
            
        Returns:
            True if successful
        """
        try:
            self._ensure_initialized()
            self.tts.tts_to_file(text=text, file_path=output_file)
            return True
        except Exception as e:
            print(f"Coqui TTS synthesis failed: {e}")
            return False
