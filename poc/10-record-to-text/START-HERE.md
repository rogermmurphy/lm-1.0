# POC 10: Record-to-Text - Setup Guide

## Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
cd poc/10-record-to-text
pip install -r requirements.txt
```

### Step 2: Test Your Microphone
```bash
python test_microphone.py
```

This will:
- List all audio devices
- Check default microphone
- Test sample rates
- Record a 3-second test

### Step 3: Start Recording!

**Option A: GUI (Recommended)**
```bash
python gui_recorder.py
```
- Click "Start Recording" button
- Speak into microphone
- Click "Stop Recording" when done
- Audio saved automatically!

**Option B: CLI**
```bash
python cli_recorder.py
```
- Press ENTER to start
- Speak into microphone
- Press ENTER to stop

---

## Features

### What You Get:
✅ Record from microphone  
✅ Real-time duration display  
✅ Auto-save to WAV file  
✅ Integration with POC 09 (auto-transcription)  
✅ GUI and CLI interfaces  

### Audio Format:
- Sample Rate: 16kHz (optimal for Whisper)
- Channels: Mono
- Format: WAV (16-bit)
- File naming: `recording_YYYYMMDD_HHMMSS.wav`

---

## Integration with POC 09

### If POC 09 is Set Up:
Recordings are **automatically queued for transcription**!

1. Record audio with POC 10
2. Audio saved to `recordings/` folder
3. Automatically queued to POC 09
4. Whisper transcribes in background
5. Transcript saved to database
6. Auto-loaded to ChromaDB for RAG

### If POC 09 is NOT Set Up:
Recordings still work! Just no auto-transcription.

To enable transcription:
```bash
# Go to POC 09
cd ../09-speech-to-text

# Follow setup guide
cat START-HERE.md
```

---

## Testing

### Test 1: Quick Audio Test
```bash
python audio_recorder.py
```
Records 5 seconds, saves to file.

### Test 2: Microphone Diagnostic
```bash
python test_microphone.py
```
Full diagnostic of audio setup.

### Test 3: CLI Recording
```bash
python cli_recorder.py
```
Record with command-line interface.

### Test 4: GUI Recording
```bash
python gui_recorder.py
```
Record with graphical interface.

---

## File Structure

```
poc/10-record-to-text/
├── audio_recorder.py      # Core recording logic
├── cli_recorder.py        # CLI interface
├── gui_recorder.py        # GUI interface
├── test_microphone.py     # Diagnostic tool
├── recordings/            # Saved recordings (auto-created)
│   └── recording_*.wav    # Your recordings
├── requirements.txt       # Python dependencies
├── README.md             # Overview
└── START-HERE.md         # This file
```

---

## Troubleshooting

### Problem: No microphone detected
**Solution:**
1. Check if microphone is plugged in
2. Check Windows sound settings (right-click speaker icon)
3. Make sure microphone is not muted
4. Try restarting the application

### Problem: Audio quality is poor
**Solution:**
1. Check microphone volume in Windows
2. Speak closer to microphone
3. Use external USB microphone (better quality)
4. Check for background noise

### Problem: "Module not found" error
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: POC 09 transcription not working
**Solution:**
Check if POC 09 services are running:
- PostgreSQL database
- Redis server
- Transcription worker

```bash
cd ../09-speech-to-text
python transcription_worker.py
```

---

## Usage Examples

### Example 1: Record a Lecture
```bash
python gui_recorder.py

# 1. Click "Start Recording"
# 2. Professor speaks for 45 minutes
# 3. Click "Stop Recording"
# 4. Wait 5-10 minutes for transcription
# 5. Search transcript in RAG system
```

### Example 2: Voice Notes
```bash
python cli_recorder.py

# Quick voice memo:
# Press ENTER → Speak → Press ENTER
# Done! Auto-transcribed.
```

### Example 3: Interview Recording
```bash
python gui_recorder.py

# 1. Start recording
# 2. Conduct interview
# 3. Stop recording
# 4. Get transcript automatically
```

---

## Audio Specifications

### Recommended Settings (Already Configured):
- **Sample Rate**: 16000 Hz
  - Optimal for Whisper AI
  - Good balance of quality and file size
  - ~1 MB per minute

- **Channels**: 1 (Mono)
  - Sufficient for speech
  - Smaller file size
  - Faster transcription

- **Bit Depth**: 16-bit
  - Standard for speech
  - Good quality
  - Wide compatibility

### File Sizes:
- 1 minute recording ≈ 1 MB
- 10 minutes ≈ 10 MB
- 1 hour ≈ 60 MB

---

## Next Steps

### After Recording:
1. ✅ Audio saved to `recordings/` folder
2. ✅ Queued for transcription (if POC 09 available)
3. ⏳ Wait 5-20 minutes for transcription
4. 📝 Check transcript in database
5. 💬 Ask questions about recorded content

### To Check Transcription Status:
```bash
cd ../09-speech-to-text
python -c "
from async_transcription_tool import AsyncTranscriptionTool
tool = AsyncTranscriptionTool()
print(tool.get_job_status('YOUR_JOB_ID'))
"
```

### To View All Recordings:
```bash
cd recordings
dir  # Windows
ls   # Mac/Linux
```

---

## Tips for Best Results

### Recording Quality:
✓ Use external USB microphone (best quality)  
✓ Record in quiet environment  
✓ Speak clearly and at normal volume  
✓ Keep microphone 6-12 inches from mouth  
✓ Avoid background music or noise  

### Transcription Accuracy:
✓ Clear speech → 95%+ accuracy  
✓ Noisy environment → 70-80% accuracy  
✓ Multiple speakers → Use separate recordings  
✓ Technical terms → May need manual correction  

---

## FAQ

**Q: Can I use Bluetooth headset?**  
A: Yes! Any Windows-compatible microphone works.

**Q: What if recording is interrupted?**  
A: Recording is saved when stopped. Just start a new recording.

**Q: Can I record stereo?**  
A: Yes, change `channels=2` in audio_recorder.py. But mono is recommended for speech.

**Q: How long can I record?**  
A: Unlimited! But consider file size (1 MB per minute).

**Q: Can I edit recordings?**  
A: Use audio editing software like Audacity. POC 10 focuses on capture.

**Q: Do I need POC 09?**  
A: No! POC 10 works standalone. POC 09 adds auto-transcription.

---

## Support

### Check Logs:
Error messages are printed to console.

### Test Each Component:
```bash
# Test microphone
python test_microphone.py

# Test recording
python audio_recorder.py

# Test CLI
python cli_recorder.py

# Test GUI
python gui_recorder.py
```

### Still Having Issues?
1. Check requirements are installed
2. Verify microphone in Windows settings
3. Try different interface (CLI vs GUI)
4. Check error messages carefully

---

## What's Next?

POC 10 is complete! You now have:
- ✅ Working audio recorder
- ✅ Two interfaces (CLI + GUI)
- ✅ Integration with POC 09
- ✅ Real-time recording

### Future Enhancements (Not in POC):
- Real-time transcription during recording
- Audio waveform visualization
- Multiple microphone support
- Audio compression (MP3)
- Cloud storage integration

---

**Ready to record? Run:**
```bash
python gui_recorder.py
```

**Questions? Check:**
- README.md - Overview and architecture
- POC-STATUS.md - Test results and status
