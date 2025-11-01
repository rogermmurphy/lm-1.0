# POC 11: Text-to-Speech Strategy

## Updated Strategy Based on User Feedback

### Key Insights

1. **Azure TTS for Development**: FREE 500k chars/month makes it ideal for POC development
2. **Little Monster Integration**: The business has defined a clear end-goal with React frontend
3. **Multi-Provider Approach**: Need flexibility to switch between providers
4. **Audio Analysis**: Mouth sync animation requires real-time audio analysis

---

## Implementation Strategy

### Phase 1: Multi-Provider TTS Engine

Build a unified TTS engine that supports all providers:

```
TTSEngine (Abstract Base)
├── AzureTTSProvider (PRIMARY for dev - FREE!)
├── OpenAITTSProvider (BEST quality for production)
├── CoquiTTSProvider (LOCAL/OFFLINE like Little Monster)
├── EdgeTTSProvider (FREE backup)
└── Pyttsx3Provider (OFFLINE fallback)
```

**Benefits**:
- Easy provider switching
- Fallback chain for reliability
- Cost optimization (use free tiers for dev)
- Production-ready quality options

---

## Provider Selection Matrix

### For POC Development (NOW)
**Primary**: Azure TTS
- ✅ FREE 500k chars/month
- ✅ SSML support for customization
- ✅ HD voices comparable to OpenAI
- ✅ Good quality for testing
- ⚠️ Some pronunciation issues (documented in research)

### For Production (FUTURE)
**Primary**: OpenAI TTS-1-HD
- ✅ Best natural quality
- ✅ No dropped words
- ✅ Production-proven
- 💰 $0.90 per 30k chars (reasonable cost)

### For Little Monster Integration
**Primary**: Coqui TTS (Jenny voice)
- ✅ LOCAL execution (no API costs)
- ✅ Real-time audio analysis
- ✅ Mouth sync capability
- ✅ Same as business requirements
- ⚠️ Requires torch/GPU for best performance

### For Offline/Fallback
**Fallback Chain**:
1. Coqui TTS (if model loaded)
2. pyttsx3 (always works offline)

---

## Architecture Diagram

```
User Text Input
      ↓
┌─────────────────────────────────────┐
│   TTS Engine (Abstraction Layer)   │
├─────────────────────────────────────┤
│  Provider Selection Strategy:       │
│  • Development: Azure (free)        │
│  • Production: OpenAI (quality)     │
│  • Local/Offline: Coqui (Little M)  │
│  • Fallback: edge-tts → pyttsx3    │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│        Audio Generation             │
│  • WAV/MP3 file output             │
│  • Streaming support               │
│  • Format conversion               │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│     Audio Analysis (Little M)       │
│  • FFT frequency analysis          │
│  • Amplitude tracking              │
│  • Mouth sync data                 │
│  • Real-time processing            │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│      Audio Playback                 │
│  • pygame for Windows              │
│  • Web Audio API (for React)       │
│  • Streaming playback              │
└─────────────────────────────────────┘
```

---

## Little Monster Integration Path

### Current Little Monster Stack
```
Backend:  Flask + Coqui TTS (Jenny)
Frontend: React + Vite + Tailwind
Feature:  Real-time mouth sync animation
```

### POC 11 → Little Monster Bridge
```
POC 11 provides:
1. Multi-provider TTS engine
2. Audio analysis utilities
3. Mouth sync data generation
4. Provider comparison tools

Little Monster uses:
1. Coqui TTS provider from POC 11
2. Audio analysis from POC 11
3. Same architecture patterns
4. Testing/comparison tools
```

---

## Implementation Phases

### Phase 1: Core TTS Engine ⚡ (PRIORITY)
**Files to Create**:
- `tts_engine.py` - Abstract base engine
- `providers/azure_tts.py` - Azure provider (PRIMARY DEV)
- `providers/openai_tts.py` - OpenAI provider (PRODUCTION)
- `providers/coqui_tts.py` - Coqui provider (LITTLE MONSTER)
- `providers/edge_tts.py` - Edge provider (FREE BACKUP)
- `providers/pyttsx3_tts.py` - Offline provider (FALLBACK)

**Key Features**:
```python
class TTSEngine:
    def speak(text: str, voice: str = None) -> bytes
    def save_to_file(text: str, filename: str, voice: str = None)
    def list_voices() -> List[Voice]
    def set_provider(provider: str)
    def get_audio_analysis(audio_data: bytes) -> AudioAnalysis
```

### Phase 2: Audio Analysis (Little Monster Feature)
**Files to Create**:
- `audio_analyzer.py` - FFT and amplitude analysis
- `mouth_sync.py` - Mouth position calculator

**Features**:
```python
class AudioAnalyzer:
    def analyze_audio(audio_file: str) -> AudioData
    def get_mouth_positions(audio_data: AudioData) -> List[MouthState]
    def get_amplitude_over_time(audio_data: AudioData) -> np.array
```

### Phase 3: CLI & Testing Tools
**Files to Create**:
- `cli_tts.py` - Command-line interface
- `test_voices.py` - Voice comparison tool
- `test_providers.py` - Provider testing

**Features**:
- Interactive voice selection
- Provider comparison
- Quality testing
- Audio sample generation

### Phase 4: Integration Examples
**Files to Create**:
- `chatbot_integration.py` - POC 00 chatbot + TTS
- `little_monster_adapter.py` - Little Monster integration helper

---

## Cost Optimization Strategy

### Development Phase (NOW)
```
Primary:  Azure TTS (FREE 500k/month)
Backup:   Coqui TTS (FREE, local)
Fallback: edge-tts (FREE)
Testing:  pyttsx3 (FREE, instant)

Total Dev Cost: $0/month! 🎉
```

### Production Phase (FUTURE)
```
Primary:  OpenAI TTS-1-HD ($0.90 per 30k chars)
Backup:   Azure TTS (FREE 500k, then $0.90 per 30k)
Local:    Coqui TTS (FREE, no API calls)

Estimated: $50-100/month for moderate use
Scale:     Add more Coqui instances for cost savings
```

---

## Quality vs Cost Matrix

| Provider | Quality | Cost | Latency | Offline | Notes |
|----------|---------|------|---------|---------|-------|
| **OpenAI TTS-1-HD** | ⭐⭐⭐⭐⭐ | $$ | Fast | ❌ | Best for production |
| **Azure HD** | ⭐⭐⭐⭐ | FREE! | Fast | ❌ | **Best for dev** |
| **Coqui (Jenny)** | ⭐⭐⭐⭐ | FREE | Medium | ✅ | **Little Monster** |
| **edge-tts** | ⭐⭐⭐½ | FREE | Fast | ❌ | Good backup |
| **pyttsx3** | ⭐⭐ | FREE | Instant | ✅ | Offline demos |

---

## Testing Strategy

### Voice Quality Testing
```python
# Generate same text with all providers
test_text = "Hello! This is a test of the text-to-speech system."

providers = ['azure', 'openai', 'coqui', 'edge', 'pyttsx3']
for provider in providers:
    tts.set_provider(provider)
    tts.save_to_file(test_text, f'samples/{provider}_sample.wav')
```

### Comparison Metrics
- [ ] Naturalness (subjective listening)
- [ ] Word accuracy (no dropped words)
- [ ] Pronunciation quality
- [ ] Emotional expressiveness
- [ ] Latency measurement
- [ ] Cost per 1000 characters

---

## Little Monster Feature: Mouth Sync

### Audio Analysis Pipeline
```python
# 1. Generate speech
audio_bytes = tts.speak("Hello world!")

# 2. Analyze audio
analyzer = AudioAnalyzer()
audio_data = analyzer.analyze_audio(audio_bytes)

# 3. Extract mouth positions
mouth_states = analyzer.get_mouth_positions(audio_data)

# 4. Output format for React
{
    "timestamps": [0, 0.1, 0.2, 0.3, ...],
    "mouth_open": [0, 45, 75, 90, ...],  # 0-100%
    "amplitude": [0, 25, 50, 30, ...]    # 0-100
}
```

### React Integration (Little Monster)
```javascript
// Use audio analysis data
const [mouthOpen, setMouthOpen] = useState(0);

useEffect(() => {
    if (audioAnalysis) {
        // Sync mouth animation with audio playback
        const syncMouth = () => {
            const currentTime = audioRef.current.currentTime;
            const index = Math.floor(currentTime * 10); // 10 fps
            setMouthOpen(audioAnalysis.mouth_open[index] || 0);
        };
        audioRef.current.addEventListener('timeupdate', syncMouth);
    }
}, [audioAnalysis]);
```

---

## Configuration Management

### Environment Variables
```bash
# Azure TTS (PRIMARY for dev)
AZURE_SPEECH_KEY=your_key_here
AZURE_SPEECH_REGION=eastus

# OpenAI (for production testing)
OPENAI_API_KEY=your_key_here

# Provider Selection
TTS_PROVIDER=azure  # azure|openai|coqui|edge|pyttsx3
TTS_VOICE=en-US-JennyNeural  # Provider-specific
```

### Config File (config.json)
```json
{
    "default_provider": "azure",
    "fallback_chain": ["azure", "coqui", "edge", "pyttsx3"],
    "providers": {
        "azure": {
            "enabled": true,
            "default_voice": "en-US-JennyNeural",
            "quality": "HD"
        },
        "openai": {
            "enabled": false,
            "default_voice": "fable",
            "model": "tts-1-hd"
        },
        "coqui": {
            "enabled": true,
            "model": "tts_models/en/jenny/jenny",
            "gpu": false
        }
    },
    "audio": {
        "format": "wav",
        "sample_rate": 22050,
        "enable_analysis": true
    }
}
```

---

## File Structure

```
poc/11-text-to-speech/
├── README.md                    # Overview
├── requirements.txt             # Dependencies (DONE)
├── TTS-RESEARCH-ANALYSIS.md     # Research findings (DONE)
├── POC-11-STRATEGY.md           # This file (DONE)
├── START-HERE.md                # Quick start guide
│
├── config.json                  # Configuration
├── config.example.json          # Example config
│
├── tts_engine.py               # Main engine (abstract base)
├── audio_analyzer.py           # Audio analysis for mouth sync
│
├── providers/                  # TTS Provider implementations
│   ├── __init__.py
│   ├── base.py                # Base provider class
│   ├── azure_tts.py           # Azure (PRIMARY DEV)
│   ├── openai_tts.py          # OpenAI (PRODUCTION)
│   ├── coqui_tts.py           # Coqui (LITTLE MONSTER)
│   ├── edge_tts.py            # Edge (FREE BACKUP)
│   └── pyttsx3_tts.py         # Pyttsx3 (OFFLINE)
│
├── cli_tts.py                 # CLI interface
├── test_voices.py             # Voice comparison tool
├── test_providers.py          # Provider testing
│
├── chatbot_integration.py     # POC 00 integration
├── little_monster_adapter.py  # Little Monster helper
│
├── samples/                   # Generated audio samples
│   ├── azure_sample.wav
│   ├── openai_sample.wav
│   └── ...
│
└── tests/                     # Test suite
    ├── test_tts_engine.py
    ├── test_providers.py
    └── test_audio_analysis.py
```

---

## Success Criteria

### POC 11 Success Metrics
- [x] Research completed and stored in Chroma
- [x] Multi-provider architecture designed
- [ ] Azure TTS working (primary dev provider)
- [ ] OpenAI TTS working (production quality)
- [ ] Coqui TTS working (Little Monster compatibility)
- [ ] Audio analysis for mouth sync working
- [ ] CLI interface functional
- [ ] Voice comparison tool complete
- [ ] Provider switching seamless
- [ ] Integration example with POC 00 chatbot
- [ ] Documentation complete
- [ ] Tests passing
- [ ] Committed to GitHub

### Little Monster Readiness
- [ ] Coqui TTS provider matches Little Monster implementation
- [ ] Audio analysis generates mouth sync data
- [ ] Format compatible with React frontend
- [ ] Performance suitable for real-time use
- [ ] Example integration provided

---

## Next Steps

1. ✅ Research complete
2. ✅ Strategy documented
3. **→ Build core TTS engine with providers**
4. **→ Test Azure TTS (primary dev)**
5. **→ Test OpenAI TTS (quality check)**
6. **→ Implement Coqui TTS (Little Monster)**
7. **→ Add audio analysis**
8. **→ Create CLI interface**
9. **→ Build comparison tools**
10. **→ Document and test**
11. **→ Commit to GitHub**

---

## Timeline Estimate

- **Phase 1** (Core Engine): 2-3 hours
- **Phase 2** (Audio Analysis): 1-2 hours  
- **Phase 3** (CLI & Testing): 1-2 hours
- **Phase 4** (Integration): 1 hour
- **Total**: 5-8 hours development time

---

## References

- TTS Research: `TTS-RESEARCH-ANALYSIS.md`
- Little Monster Requirements: User-provided spec
- Chroma Database: `ai_ml_comprehensive_docs` collection
- Azure TTS Docs: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/
- OpenAI TTS Docs: https://platform.openai.com/docs/guides/text-to-speech
- Coqui TTS: https://github.com/coqui-ai/TTS

---

## Conclusion

POC 11 takes a pragmatic, cost-effective approach:
- **Use Azure FREE tier for all development**
- **Keep OpenAI ready for production quality**
- **Incorporate Coqui for Little Monster integration**
- **Build flexibility to switch providers**
- **Add audio analysis for advanced features**

This strategy balances quality, cost, and business requirements perfectly.

**Let's build it! 🚀**
