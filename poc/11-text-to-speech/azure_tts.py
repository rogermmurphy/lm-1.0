"""
POC 11: Azure Text-to-Speech Provider
Leverages Azure's FREE 500k characters/month tier for cost-effective TTS.
"""

import os
from pathlib import Path
from typing import Optional, List
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load environment variables from .env file
load_dotenv()


class AzureTTS:
    """
    Azure Text-to-Speech provider.
    
    Features:
    - FREE 500k characters/month
    - HD quality voices
    - SSML support
    - Multiple languages
    
    Setup:
    1. Get free Azure Speech API key: https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/
    2. Set environment variables:
       - AZURE_SPEECH_KEY=your_key
       - AZURE_SPEECH_REGION=eastus (or your region)
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        region: Optional[str] = None,
        voice: str = "en-US-JennyNeural"
    ):
        """
        Initialize Azure TTS.
        
        Args:
            api_key: Azure Speech API key (or set AZURE_SPEECH_KEY env var)
            region: Azure region (or set AZURE_SPEECH_REGION env var)
            voice: Voice name (default: en-US-JennyNeural)
        """
        self.api_key = api_key or os.getenv('AZURE_SPEECH_KEY')
        self.region = region or os.getenv('AZURE_SPEECH_REGION', 'eastus')
        self.voice = voice
        
        if not self.api_key:
            raise ValueError(
                "Azure Speech API key required. "
                "Set AZURE_SPEECH_KEY environment variable or pass api_key parameter."
            )
        
        # Initialize speech config
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.api_key,
            region=self.region
        )
        self.speech_config.speech_synthesis_voice_name = self.voice
        
        # Audio configuration for file output
        # Will be set per synthesis call
        self.audio_config = None
    
    def speak(self, text: str, output_file: str = "output.wav") -> bool:
        """
        Convert text to speech and save to file.
        
        Args:
            text: Text to convert to speech
            output_file: Output audio file path (default: output.wav)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Configure audio output to file
            self.audio_config = speechsdk.audio.AudioOutputConfig(
                filename=output_file
            )
            
            # Create synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=self.audio_config
            )
            
            # Synthesize
            result = synthesizer.speak_text_async(text).get()
            
            # Check result
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print(f"[SUCCESS] Speech synthesized: {output_file}")
                print(f"   Characters used: {len(text)}")
                return True
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                print(f"[ERROR] Speech synthesis canceled: {cancellation.reason}")
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    print(f"   Error: {cancellation.error_details}")
                return False
            else:
                print(f"[ERROR] Unexpected result: {result.reason}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error during speech synthesis: {e}")
            return False
    
    def speak_ssml(self, ssml: str, output_file: str = "output.wav") -> bool:
        """
        Convert SSML to speech and save to file.
        
        SSML (Speech Synthesis Markup Language) allows fine control over:
        - Pronunciation
        - Pitch, rate, volume
        - Pauses and breaks
        - Emphasis
        
        Example SSML:
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
                <voice name="en-US-JennyNeural">
                    Hello! <break time="500ms"/> 
                    This is <emphasis level="strong">important</emphasis>.
                </voice>
            </speak>
        
        Args:
            ssml: SSML markup
            output_file: Output audio file path
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.audio_config = speechsdk.audio.AudioOutputConfig(
                filename=output_file
            )
            
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=self.audio_config
            )
            
            result = synthesizer.speak_ssml_async(ssml).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print(f"[SUCCESS] SSML synthesized: {output_file}")
                return True
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                print(f"[ERROR] SSML synthesis canceled: {cancellation.reason}")
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    print(f"   Error: {cancellation.error_details}")
                return False
            else:
                print(f"[ERROR] Unexpected result: {result.reason}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error during SSML synthesis: {e}")
            return False
    
    def list_voices(self) -> List[dict]:
        """
        List all available voices for the configured region.
        
        Returns:
            List of voice information dictionaries
        """
        try:
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config, 
                audio_config=None
            )
            
            result = synthesizer.get_voices_async().get()
            
            if result.reason == speechsdk.ResultReason.VoicesListRetrieved:
                voices = []
                for voice in result.voices:
                    voices.append({
                        'name': voice.short_name,
                        'full_name': voice.name,
                        'locale': voice.locale,
                        'gender': voice.gender.name if voice.gender else 'Unknown',
                        'local_name': voice.local_name
                    })
                return voices
            else:
                print(f"[ERROR] Failed to retrieve voices: {result.reason}")
                return []
                
        except Exception as e:
            print(f"[ERROR] Error listing voices: {e}")
            return []
    
    def set_voice(self, voice: str):
        """
        Change the voice for synthesis.
        
        Args:
            voice: Voice name (e.g., "en-US-JennyNeural")
        """
        self.voice = voice
        self.speech_config.speech_synthesis_voice_name = voice
        print(f"[INFO] Voice changed to: {voice}")


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("POC 11: Azure TTS Test")
    print("=" * 60)
    
    # Check environment variables
    if not os.getenv('AZURE_SPEECH_KEY'):
        print("\n[ERROR] Missing AZURE_SPEECH_KEY environment variable!")
        print("\nSetup Instructions:")
        print("1. Go to: https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/")
        print("2. Create a free Azure Speech resource")
        print("3. Set environment variables:")
        print("   - AZURE_SPEECH_KEY=your_key")
        print("   - AZURE_SPEECH_REGION=eastus (or your region)")
        print("\nWindows (CMD):")
        print("   set AZURE_SPEECH_KEY=your_key")
        print("   set AZURE_SPEECH_REGION=eastus")
        print("\nWindows (PowerShell):")
        print("   $env:AZURE_SPEECH_KEY='your_key'")
        print("   $env:AZURE_SPEECH_REGION='eastus'")
        exit(1)
    
    # Initialize TTS
    tts = AzureTTS()
    print(f"\n[SUCCESS] Azure TTS initialized")
    print(f"   Region: {tts.region}")
    print(f"   Voice: {tts.voice}")
    
    # Test basic synthesis
    print("\n" + "=" * 60)
    print("Test 1: Basic Text-to-Speech")
    print("=" * 60)
    test_text = "Hello! This is a test of Azure Text-to-Speech. How do I sound?"
    tts.speak(test_text, "test_basic.wav")
    
    # Test with different voice
    print("\n" + "=" * 60)
    print("Test 2: Different Voice")
    print("=" * 60)
    tts.set_voice("en-US-GuyNeural")
    tts.speak("This is Guy's voice. Nice to meet you!", "test_guy.wav")
    
    # Test SSML
    print("\n" + "=" * 60)
    print("Test 3: SSML with Emphasis")
    print("=" * 60)
    tts.set_voice("en-US-JennyNeural")
    ssml = """
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
        <voice name="en-US-JennyNeural">
            This is <emphasis level="strong">very important</emphasis> information.
            <break time="500ms"/>
            Please listen carefully.
        </voice>
    </speak>
    """
    tts.speak_ssml(ssml, "test_ssml.wav")
    
    # List available voices
    print("\n" + "=" * 60)
    print("Available Voices (first 10):")
    print("=" * 60)
    voices = tts.list_voices()
    for i, voice in enumerate(voices[:10]):
        print(f"{i+1}. {voice['name']} ({voice['locale']}) - {voice['gender']}")
    print(f"\n... and {len(voices) - 10} more voices")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] All tests complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - test_basic.wav (Jenny voice)")
    print("  - test_guy.wav (Guy voice)")
    print("  - test_ssml.wav (SSML example)")
    print("\nCost: $0 (using FREE 500k chars/month tier)")
