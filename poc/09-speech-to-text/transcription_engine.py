#!/usr/bin/env python3
"""
Transcription Engine - Core Whisper transcription functionality
Handles audio file transcription using faster-whisper
"""

import os
import time
from pathlib import Path
from typing import Dict, Optional
from faster_whisper import WhisperModel

class TranscriptionEngine:
    """
    Core transcription engine using faster-whisper
    Provides efficient local speech-to-text conversion
    """
    
    def __init__(self, model_size: str = "base", device: str = "cpu"):
        """
        Initialize Whisper model
        
        Args:
            model_size: Model size (tiny, base, small, medium, large)
            device: Device to run on (cpu or cuda)
        """
        self.model_size = model_size
        self.device = device
        self.model = None
        
        print(f"[WHISPER] Initializing {model_size} model on {device}...")
        
    def load_model(self):
        """Load the Whisper model (lazy loading)"""
        if self.model is None:
            self.model = WhisperModel(self.model_size, device=self.device)
            print(f"[OK] Model loaded: {self.model_size}")
    
    def transcribe_file(self, 
                       audio_path: str,
                       language: Optional[str] = None,
                       return_timestamps: bool = True) -> Dict:
        """
        Transcribe an audio file
        
        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'en', 'es') or None for auto-detect
            return_timestamps: Whether to include timestamps
            
        Returns:
            Dictionary with transcription results
        """
        # Load model if not loaded
        self.load_model()
        
        # Validate file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
        print(f"\n[TRANSCRIBE] File: {audio_path}")
        print(f"[TRANSCRIBE] Size: {file_size_mb:.2f} MB")
        
        # Start transcription
        start_time = time.time()
        
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            word_timestamps=return_timestamps
        )
        
        # Process segments
        transcript_text = ""
        segment_list = []
        
        for segment in segments:
            transcript_text += segment.text + " "
            
            if return_timestamps:
                segment_list.append({
                    'start': round(segment.start, 2),
                    'end': round(segment.end, 2),
                    'text': segment.text.strip()
                })
        
        elapsed_time = time.time() - start_time
        
        # Compile results
        result = {
            'text': transcript_text.strip(),
            'language': info.language,
            'language_probability': round(info.language_probability, 2),
            'duration': round(info.duration, 2),
            'processing_time': round(elapsed_time, 2),
            'model_size': self.model_size
        }
        
        if return_timestamps:
            result['segments'] = segment_list
            result['num_segments'] = len(segment_list)
        
        # Performance metrics
        if info.duration > 0:
            rtf = elapsed_time / info.duration  # Real-time factor
            result['real_time_factor'] = round(rtf, 2)
        
        print(f"[OK] Transcription complete")
        print(f"[OK] Language: {info.language} ({info.language_probability:.1%})")
        print(f"[OK] Duration: {info.duration:.1f}s")
        print(f"[OK] Processing: {elapsed_time:.1f}s")
        if info.duration > 0:
            print(f"[OK] Speed: {rtf:.2f}x realtime")
        
        return result
    
    def transcribe_with_speaker_labels(self, audio_path: str) -> Dict:
        """
        Transcribe with basic speaker detection
        (Note: True speaker diarization requires additional libraries)
        """
        result = self.transcribe_file(audio_path, return_timestamps=True)
        
        # Simple speaker detection based on pause length
        segments = result.get('segments', [])
        labeled_segments = []
        current_speaker = 1
        
        for i, segment in enumerate(segments):
            # If long pause (>2 seconds), assume speaker change
            if i > 0:
                prev_end = segments[i-1]['end']
                curr_start = segment['start']
                if curr_start - prev_end > 2.0:
                    current_speaker = 2 if current_speaker == 1 else 1
            
            labeled_segments.append({
                'speaker': f'Speaker {current_speaker}',
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text']
            })
        
        result['segments'] = labeled_segments
        return result
    
    def get_summary(self, audio_path: str) -> str:
        """
        Get quick summary of transcription (text only, no timestamps)
        """
        result = self.transcribe_file(audio_path, return_timestamps=False)
        return result['text']


# Test/demo functions
def test_transcription():
    """Test transcription with a sample file"""
    engine = TranscriptionEngine(model_size="base")
    
    # You would replace this with an actual audio file path
    print("\n" + "="*70)
    print("TRANSCRIPTION ENGINE TEST")
    print("="*70)
    print("\nTo test:")
    print("1. Place an audio file (MP3, WAV, etc.) in this directory")
    print("2. Update the path below in this script")
    print("3. Run: python transcription_engine.py")
    print("\nExample:")
    print("  result = engine.transcribe_file('sample_lecture.mp3')")
    print("  print(result['text'])")
    

if __name__ == "__main__":
    test_transcription()
