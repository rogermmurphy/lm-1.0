"""
POC 11.1: Coqui TTS Implementation
Using the official Little Monster spec: Jenny voice model
"""

import time
from TTS.api import TTS

class CoquiTTS:
    """
    Coqui TTS provider - matching Little Monster specification.
    Uses tts_models/en/jenny/jenny model.
    """
    
    def __init__(self, model_name="tts_models/en/jenny/jenny", gpu=False):
        """
        Initialize Coqui TTS with Jenny voice model.
        
        Args:
            model_name: TTS model to use (default: jenny)
            gpu: Use GPU if available (default: False for CPU)
        """
        print(f"[INFO] Initializing Coqui TTS...")
        print(f"[INFO] Model: {model_name}")
        print(f"[INFO] GPU: {gpu}")
        
        self.model_name = model_name
        self.gpu = gpu
        
        # Initialize TTS - will download model on first use
        self.tts = TTS(model_name=model_name, progress_bar=False, gpu=gpu)
        
        print(f"[SUCCESS] Coqui TTS initialized")
    
    def speak(self, text, output_file="output.wav"):
        """
        Convert text to speech and save to file.
        
        Args:
            text: Text to convert to speech
            output_file: Output audio file path
            
        Returns:
            bool: True if successful
        """
        try:
            start_time = time.time()
            
            # Generate speech
            self.tts.tts_to_file(text=text, file_path=output_file)
            
            generation_time = time.time() - start_time
            
            print(f"[SUCCESS] Speech synthesized: {output_file}")
            print(f"   Characters: {len(text)}")
            print(f"   Generation time: {generation_time:.3f}s")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to generate speech: {e}")
            return False
    
    def list_models(self):
        """List all available Coqui TTS models."""
        print("\n[INFO] Available Coqui TTS Models:")
        models = TTS().list_models()
        for model in models:
            print(f"  - {model}")
        return models


if __name__ == "__main__":
    print("=" * 60)
    print("POC 11.1: Coqui TTS Test")
    print("=" * 60)
    
    # Initialize with Jenny model
    tts = CoquiTTS()
    
    # Test 1: Basic synthesis
    print("\n" + "=" * 60)
    print("Test 1: Basic Text-to-Speech")
    print("=" * 60)
    test_text = "Hello! This is a test of Coqui Text-to-Speech using the Jenny voice model."
    tts.speak(test_text, "coqui_test_basic.wav")
    
    # Test 2: Medium length
    print("\n" + "=" * 60)
    print("Test 2: Medium Length")
    print("=" * 60)
    medium_text = "The quick brown fox jumps over the lazy dog. This is a test of Coqui TTS with a medium-length sentence to compare performance."
    tts.speak(medium_text, "coqui_test_medium.wav")
    
    # Test 3: Long text
    print("\n" + "=" * 60)
    print("Test 3: Long Text")
    print("=" * 60)
    long_text = """
    Coqui TTS is an open-source deep learning toolkit for text-to-speech generation.
    It provides pretrained models in over one thousand languages and tools for training
    new models. The library is designed for both research and production use cases.
    """
    tts.speak(long_text, "coqui_test_long.wav")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] All tests complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - coqui_test_basic.wav")
    print("  - coqui_test_medium.wav")
    print("  - coqui_test_long.wav")
    print("\nCost: $0 (local execution)")
