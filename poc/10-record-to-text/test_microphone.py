"""
POC 10: Microphone Test Utility
Test microphone detection and audio input
"""
import sounddevice as sd
import numpy as np
import sys


def list_all_devices():
    """List all audio devices (input and output)"""
    print("\n" + "="*60)
    print("ALL AUDIO DEVICES")
    print("="*60)
    
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"\nDevice {i}: {device['name']}")
        print(f"  Max Input Channels:  {device['max_input_channels']}")
        print(f"  Max Output Channels: {device['max_output_channels']}")
        print(f"  Default Sample Rate: {device['default_samplerate']:.0f} Hz")


def list_input_devices():
    """List only input devices (microphones)"""
    print("\n" + "="*60)
    print("INPUT DEVICES (MICROPHONES)")
    print("="*60)
    
    devices = sd.query_devices()
    input_devices = []
    
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            input_devices.append((i, device))
            print(f"\n✓ Device {i}: {device['name']}")
            print(f"  Channels: {device['max_input_channels']}")
            print(f"  Sample Rate: {device['default_samplerate']:.0f} Hz")
    
    if not input_devices:
        print("\n❌ No input devices found!")
        return None
    
    return input_devices


def get_default_input():
    """Get default input device"""
    print("\n" + "="*60)
    print("DEFAULT INPUT DEVICE")
    print("="*60)
    
    try:
        device = sd.query_devices(kind='input')
        print(f"\n✓ {device['name']}")
        print(f"  Channels: {device['max_input_channels']}")
        print(f"  Sample Rate: {device['default_samplerate']:.0f} Hz")
        return device
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def test_microphone_input(duration=3):
    """
    Test microphone input by recording for a few seconds
    and showing audio level
    """
    print("\n" + "="*60)
    print("MICROPHONE INPUT TEST")
    print("="*60)
    
    print(f"\nRecording {duration} seconds to test microphone...")
    print("Speak into your microphone!\n")
    
    try:
        # Record audio
        recording = sd.rec(
            int(duration * 16000),
            samplerate=16000,
            channels=1,
            dtype='int16'
        )
        sd.wait()  # Wait until recording is finished
        
        # Calculate audio levels
        audio_array = np.array(recording)
        max_amplitude = np.max(np.abs(audio_array))
        avg_amplitude = np.mean(np.abs(audio_array))
        
        print("Recording complete!\n")
        print("Audio Levels:")
        print(f"  Max Amplitude: {max_amplitude}")
        print(f"  Avg Amplitude: {avg_amplitude:.1f}")
        
        # Determine if audio was detected
        if max_amplitude > 1000:
            print("\n✅ PASS - Microphone is working!")
            print("   Good audio levels detected.")
        elif max_amplitude > 100:
            print("\n⚠️  WARNING - Microphone working but very quiet")
            print("   Try speaking louder or checking microphone volume.")
        else:
            print("\n❌ FAIL - No audio detected")
            print("   Check if microphone is connected and not muted.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing microphone: {e}")
        return False


def check_sample_rates():
    """Check supported sample rates for default input device"""
    print("\n" + "="*60)
    print("SAMPLE RATE COMPATIBILITY")
    print("="*60)
    
    sample_rates = [8000, 16000, 22050, 44100, 48000]
    
    try:
        device = sd.query_devices(kind='input')
        device_id = sd.default.device[0]
        
        print(f"\nTesting sample rates for: {device['name']}\n")
        
        for rate in sample_rates:
            try:
                sd.check_input_settings(
                    device=device_id,
                    samplerate=rate,
                    channels=1
                )
                print(f"  ✓ {rate} Hz - Supported")
            except Exception:
                print(f"  ✗ {rate} Hz - Not supported")
        
        print("\n💡 Recommendation: Use 16000 Hz (optimal for Whisper)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def main():
    """Run all microphone tests"""
    print("\n" + "="*60)
    print("POC 10: MICROPHONE DIAGNOSTIC TEST")
    print("="*60)
    
    # Test 1: List all devices
    list_all_devices()
    
    # Test 2: List input devices
    input_devices = list_input_devices()
    
    # Test 3: Get default input
    default_input = get_default_input()
    
    # Test 4: Check sample rates
    check_sample_rates()
    
    # Test 5: Test microphone input
    if default_input:
        print("\n" + "="*60)
        input("\nPress ENTER to test microphone input (will record 3 seconds)...")
        test_microphone_input(duration=3)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    if input_devices and default_input:
        print("\n✅ All tests passed!")
        print("   Your microphone is ready for recording.")
        print("\n📝 Next steps:")
        print("   1. Run: python cli_recorder.py")
        print("   2. Or run: python gui_recorder.py")
    else:
        print("\n❌ Tests failed!")
        print("   Please check your microphone connection.")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if microphone is plugged in")
        print("   2. Check Windows sound settings")
        print("   3. Make sure microphone is not muted")
        print("   4. Try restarting the application")


if __name__ == "__main__":
    main()
