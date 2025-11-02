"""
Text-to-Speech Service - Azure TTS Service
Extracted from POC 11 - Tested with REAL Azure credentials
"""
import os
import azure.cognitiveservices.speech as speechsdk
from ..config import settings


class AzureTTSService:
    """Azure Text-to-Speech service"""
    
    def __init__(self):
        """Initialize Azure TTS with REAL credentials"""
        if not settings.AZURE_SPEECH_KEY:
            raise ValueError("AZURE_SPEECH_KEY required")
        
        self.speech_config = speechsdk.SpeechConfig(
            subscription=settings.AZURE_SPEECH_KEY,
            region=settings.AZURE_SPEECH_REGION
        )
        self.speech_config.speech_synthesis_voice_name = settings.DEFAULT_VOICE
    
    def synthesize(self, text: str, output_file: str, voice: str = None) -> bool:
        """
        Convert text to speech using Azure
        
        Args:
            text: Text to convert
            output_file: Output file path
            voice: Optional voice name
            
        Returns:
            True if successful
        """
        if voice:
            self.speech_config.speech_synthesis_voice_name = voice
        
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )
        
        result = synthesizer.speak_text_async(text).get()
        
        return result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted
