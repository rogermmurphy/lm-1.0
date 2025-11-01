"""
POC 10: Audio Recorder
Core audio recording functionality using sounddevice
"""
import sounddevice as sd
import numpy as np
import wave
import time
from pathlib import Path
from datetime import datetime
from typing import Optional


class AudioRecorder:
    """
    Core audio recording class
    Records audio from microphone and saves to WAV file
    """
    
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        dtype: str = 'int16'
    ):
        """
        Initialize audio recorder
        
        Args:
            sample_rate: Sample rate in Hz (16000 optimal for Whisper)
            channels: Number of audio channels (1=mono, 2=stereo)
            dtype: Data type for audio samples
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.dtype = dtype
        self.recording = False
        self.audio_data = []
        self.start_time = None
        
    def list_devices(self):
        """List all available audio input devices"""
        print("\n=== Available Audio Devices ===")
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                print(f"{i}: {device['name']}")
                print(f"   Channels: {device['max_input_channels']}")
                print(f"   Sample Rate: {device['default_samplerate']}")
                print()
        return devices
    
    def get_default_device(self):
        """Get default input device"""
        device = sd.query_devices(kind='input')
        print(f"\nDefault Input Device: {device['name']}")
        return device
    
    def start_recording(self):
        """Start recording audio from microphone"""
        if self.recording:
            print("Already recording!")
            return
        
        self.recording = True
        self.audio_data = []
        self.start_time = time.time()
        
        # Audio callback function
        def audio_callback(indata, frames, time_info, status):
            if status:
                print(f"Status: {status}")
            if self.recording:
                self.audio_data.append(indata.copy())
        
        # Start the input stream
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype,
            callback=audio_callback
        )
        self.stream.start()
        print(f"\n🎤 Recording started at {self.sample_rate}Hz, {self.channels} channel(s)")
    
    def stop_recording(self) -> Optional[np.ndarray]:
        """
        Stop recording and return audio data
        
        Returns:
            numpy array of audio data, or None if not recording
        """
        if not self.recording:
            print("Not recording!")
            return None
        
        self.recording = False
        self.stream.stop()
        self.stream.close()
        
        duration = time.time() - self.start_time
        print(f"⏹️  Recording stopped. Duration: {duration:.2f} seconds")
        
        # Concatenate all audio chunks
        if self.audio_data:
            audio_array = np.concatenate(self.audio_data, axis=0)
            return audio_array
        return None
    
    def save_to_file(
        self,
        audio_data: np.ndarray,
        output_dir: str = "recordings",
        filename: Optional[str] = None
    ) -> str:
        """
        Save audio data to WAV file
        
        Args:
            audio_data: numpy array of audio samples
            output_dir: Directory to save file
            filename: Optional filename (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
        
        filepath = output_path / filename
        
        # Save as WAV file
        with wave.open(str(filepath), 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 2 bytes for int16
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())
        
        file_size = filepath.stat().st_size / 1024  # KB
        print(f"💾 Saved to: {filepath} ({file_size:.1f} KB)")
        
        return str(filepath)
    
    def get_duration(self) -> float:
        """Get current recording duration in seconds"""
        if self.start_time:
            return time.time() - self.start_time
        return 0.0
    
    def record_for_duration(self, duration_seconds: float) -> Optional[np.ndarray]:
        """
        Record audio for a specific duration
        
        Args:
            duration_seconds: Duration to record in seconds
            
        Returns:
            numpy array of audio data
        """
        print(f"Recording for {duration_seconds} seconds...")
        self.start_recording()
        time.sleep(duration_seconds)
        audio_data = self.stop_recording()
        return audio_data


def test_recording():
    """Test the audio recorder with a 5-second recording"""
    print("\n=== Testing Audio Recorder ===")
    
    recorder = AudioRecorder()
    
    # List devices
    recorder.list_devices()
    recorder.get_default_device()
    
    # Record for 5 seconds
    print("\nRecording 5 seconds of audio...")
    audio_data = recorder.record_for_duration(5.0)
    
    if audio_data is not None:
        # Save to file
        filepath = recorder.save_to_file(audio_data)
        print(f"\n✅ Test complete! Audio saved to: {filepath}")
        print(f"   Duration: {len(audio_data) / recorder.sample_rate:.2f} seconds")
        print(f"   Samples: {len(audio_data)}")
    else:
        print("\n❌ No audio data recorded")


if __name__ == "__main__":
    test_recording()
