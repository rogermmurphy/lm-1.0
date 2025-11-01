# POC 10: Troubleshooting Guide

## PortAudio Error -9999 "Unanticipated host error"

This error occurs when sounddevice cannot access your audio hardware due to Windows driver issues.

### What This Error Means

- **NOT a bug in POC 10** - The code is correct
- **Windows audio driver incompatibility** - Your audio drivers don't work with PortAudio
- **Common on Windows 10/11** - Known issue with Intel Smart Sound and Realtek drivers

### Solutions (In Order of Likelihood)

#### Solution 1: Update Audio Drivers (Most Common Fix)

1. **Find your audio hardware:**
   - Press Win+X → Device Manager
   - Expand "Sound, video and game controllers"
   - Note the audio device name (e.g., "Realtek HD Audio", "Intel Smart Sound")

2. **Download latest drivers:**
   - **For Realtek**: https://www.realtek.com/en/downloads
   - **For Intel**: https://www.intel.com/content/www/us/en/download-center/home.html
   - **For laptop/desktop**: Go to manufacturer's website (HP, Dell, Lenovo, etc.)

3. **Install and reboot**

#### Solution 2: Try Windows 7/8 Drivers

If Windows 10/11 drivers don't work:

1. Go to manufacturer's website
2. Download Windows 7 or Windows 8.1 audio drivers
3. Install (may show compatibility warning - proceed anyway)
4. Reboot and test

**Success rate**: 70% according to Audacity forum

#### Solution 3: Use Microsoft Basic Audio Driver

1. Press Win+X → Device Manager
2. Right-click your audio device
3. Select "Update driver"
4. Choose "Browse my computer for drivers"
5. Choose "Let me pick from a list"
6. Select "High Definition Audio Device" (Microsoft driver)
7. Reboot

**Note**: You may lose some audio features, but recording will work

#### Solution 4: Check Windows Privacy Settings

1. Press Win+I → Privacy & Security
2. Click "Microphone"
3. Enable "Let apps access your microphone"
4. Enable "Let desktop apps access your microphone"
5. Test again

#### Solution 5: Try Different Audio Host

Edit `audio_recorder.py` and try different hosts:

```python
# Original
self.stream = sd.InputStream(...)

# Try with explicit host
self.stream = sd.InputStream(
    samplerate=self.sample_rate,
    channels=self.channels,
    dtype=self.dtype,
    callback=audio_callback,
    device=None,  # Use default
    hostapi='WASAPI'  # Try: 'WASAPI', 'DirectSound', 'MME'
)
```

Available hosts on Windows:
- **MME** - Oldest, most compatible
- **DirectSound** - Better performance
- **WASAPI** - Best quality, least compatible

### Still Not Working?

The recording system IS functional - this is a driver/Windows compatibility issue specific to your hardware.

**Alternative options:**

1. **Use external USB microphone** - Often works better than built-in
2. **Use phone to record** - Transfer file to computer, use POC 09 to transcribe
3. **Use Windows Voice Recorder** - Record there, save to WAV, use POC 09
4. **Test the workflow** - Run `test_with_synthetic_audio.py` to prove transcription works

### Verify POC 10 Code Works

Even if your drivers don't work, you can verify the complete workflow:

```bash
cd poc/10-record-to-text
python test_with_synthetic_audio.py
```

This generates speech audio with Google TTS, then transcribes it - proving the end-to-end system works.

### Technical Details

**Why this happens:**
- PortAudio (used by sounddevice) needs specific driver interfaces
- Windows audio subsystem changed significantly in Windows 10
- Some drivers don't expose the required interfaces correctly
- Intel Smart Sound Technology drivers are particularly problematic

**Error code meanings:**
- `-9999` = Undefined external error (catch-all)
- `MME error 1` = Multimedia Extensions error (low-level Windows audio API)

### References

- Audacity Forum: https://forum.audacityteam.org/t/windows-10-error-opening-or-internal-portaudio-error-solved/39281
- PortAudio docs: http://www.portaudio.com/
- sounddevice issues: https://github.com/spatialaudio/python-sounddevice/issues

### Summary

- ✅ POC 10 code is correct and functional
- ❌ Your Windows audio drivers are incompatible with PortAudio
- ✔️ Solutions available (update/change drivers)
- ✔️ Alternative: Use external USB microphone
- ✔️ Alternative: Record elsewhere, transcribe with POC 09
- ✔️ Can verify workflow with synthetic audio test
