# START HERE: POC 11 Text-to-Speech Setup

## ⚡ Quick Setup (2 minutes)

### Step 1: Install Dependencies
```bash
cd poc/11-text-to-speech
pip install -r requirements.txt
```

### Step 2: Set Your Azure Credentials

You have an Azure Speech API key ready! Set it as environment variable:

**Option A: Windows CMD**
```cmd
set AZURE_SPEECH_KEY=your_api_key_here
set AZURE_SPEECH_REGION=eastus
```

**Option B: Windows PowerShell**
```powershell
$env:AZURE_SPEECH_KEY="your_api_key_here"
$env:AZURE_SPEECH_REGION="eastus"
```

**Option C: Create .env file (Recommended)**
```bash
# Copy example and edit
copy .env.example .env
# Then edit .env file with your credentials
```

### Step 3: Test It!

**Test 1: Basic TTS**
```bash
python cli_tts.py "Hello! This is a test of Azure Text-to-Speech."
```
✅ Should create `output.wav` file

**Test 2: List Available Voices**
```bash
python cli_tts.py --list-voices
```
✅ Should show 100+ voices

**Test 3: Different Voice**
```bash
python cli_tts.py "Hi, I'm Guy!" -v en-US-GuyNeural -o guy.wav
```
✅ Should create `guy.wav` with male voice

**Test 4: Python API**
```bash
python azure_tts.py
```
✅ Should run all tests and create 3 wav files

## 🎯 Your Azure Configuration

Your Speech Service is configured for:
- **Region**: `eastus`
- **STT Endpoint**: https://eastus.stt.speech.microsoft.com
- **TTS Endpoint**: https://eastus.tts.speech.microsoft.com
- **Free Tier**: 500,000 characters/month
- **Documentation**: https://ai.azure.com/doc/azure/ai-services/reference/sdk-package-resources

## 📝 Common Use Cases

### Use Case 1: Convert Text File to Speech
```bash
# Create a text file
echo "This is my narration script." > script.txt

# Convert to speech
python cli_tts.py -f script.txt -o narration.wav
```

### Use Case 2: Different Voices
```bash
# Jenny (friendly female)
python cli_tts.py "Hello!" -v en-US-JennyNeural -o jenny.wav

# Guy (professional male)
python cli_tts.py "Hello!" -v en-US-GuyNeural -o guy.wav

# Aria (expressive female)
python cli_tts.py "Hello!" -v en-US-AriaNeural -o aria.wav
```

### Use Case 3: Python Integration
```python
from azure_tts import AzureTTS

# Initialize
tts = AzureTTS()

# Basic synthesis
tts.speak("Hello, world!", "greeting.wav")

# Change voice
tts.set_voice("en-US-GuyNeural")
tts.speak("Now in Guy's voice", "guy_greeting.wav")

# SSML for emphasis
ssml = """
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-JennyNeural">
        This is <emphasis level="strong">very important</emphasis>!
    </voice>
</speak>
"""
tts.speak_ssml(ssml, "emphasis.wav")
```

## 🔍 Troubleshooting

### Error: "Missing AZURE_SPEECH_KEY"
✅ **Fix**: Set environment variable (see Step 2 above)

### Error: "Invalid subscription key"
❌ Check your API key is correct
❌ Verify it's the Speech API key, not another Azure key
✅ Try re-copying from Azure portal

### No audio output
❌ Check file was created (`dir` to list files)
❌ Verify file size is > 0 bytes
✅ Try playing with Windows Media Player or VLC

### Poor quality
❌ Use Neural voices (names ending in "Neural")
✅ Try different voices: `python cli_tts.py --list-voices`

## 💰 Usage Tracking

Monitor your usage in Azure Portal:
1. Go to https://portal.azure.com
2. Navigate to your Speech resource
3. Check Metrics → Total Calls

**Free Tier Limit**: 500,000 characters/month
- Average sentence: ~50 characters
- **You can generate ~10,000 sentences/month FREE!**

## 📚 Next Steps

1. ✅ **Test basic TTS** - Run the Quick Setup above
2. 📖 **Read README.md** - Complete feature documentation
3. 🔬 **Explore voices** - Try different voices for your use case
4. 🎨 **Learn SSML** - Add emphasis, pauses, pronunciation
5. 🚀 **See BACKLOG.md** - Future enhancements (OpenAI, Coqui, etc.)

## 🎓 Learning Resources

### Azure Documentation
- **Speech Service**: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/
- **SSML Reference**: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup
- **Voice Gallery**: https://speech.microsoft.com/portal/voicegallery

### POC Documentation
- **README.md** - Complete overview
- **TTS-RESEARCH-ANALYSIS.md** - Why we chose Azure
- **POC-11-STRATEGY.md** - Architecture & future plans
- **BACKLOG.md** - Roadmap for additional features

## ⚠️ Security Note

**DO NOT commit your API key to GitHub!**

The `.gitignore` already excludes:
- `.env` files
- Any files with credentials

Keep your API key secure:
- ✅ Use environment variables
- ✅ Use .env file (already gitignored)
- ❌ Don't hardcode in Python files
- ❌ Don't commit to version control

## 🎉 Success Checklist

- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Basic test successful (`output.wav` created)
- [ ] Voice list displayed
- [ ] Different voices tested
- [ ] Python API test passed
- [ ] Understand free tier limits
- [ ] Know where to find docs

## 🆘 Need Help?

1. **Check Troubleshooting section above**
2. **Review README.md** for detailed examples
3. **Check Azure Portal** for service status
4. **Review error messages** carefully
5. **Test with simple text first** before complex examples

---

**You're all set!** 🚀

Run `python cli_tts.py "Hello, world!"` to get started!
