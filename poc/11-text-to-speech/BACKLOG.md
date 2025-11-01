# POC 11: Text-to-Speech Backlog

## Current Implementation
✅ **Azure TTS** - Primary implementation (FREE 500k chars/month)

## Future Provider Implementations

### Priority 1: Production-Ready Providers

#### 1. OpenAI TTS-1-HD
**Status**: Research Complete, Ready to Implement  
**Priority**: HIGH (Production Quality)  
**Effort**: 2-3 hours  

**Why**:
- Best quality in research (⭐⭐⭐⭐⭐)
- Production-proven
- Simple API
- No dropped words/glitches

**Blockers**: None  
**Cost**: $0.90 per 30k chars  
**Files Needed**:
- `providers/openai_tts.py`
- Update `tts_engine.py` to support OpenAI
- Tests

**Implementation Notes**:
```python
from openai import OpenAI
client = OpenAI()
response = client.audio.speech.create(
    model="tts-1-hd",
    voice="fable",  # or alloy, echo, onyx, nova, shimmer, sage, coral
    input=text
)
```

---

#### 2. Coqui TTS (Little Monster Compatibility)
**Status**: Verified Real (43.2k GitHub stars), Not Yet Implemented  
**Priority**: MEDIUM (Little Monster integration)  
**Effort**: 4-6 hours (includes testing, audio analysis)

**Why**:
- Required for Little Monster React app
- Local execution (no API costs)
- Audio analysis for mouth sync
- Jenny voice model

**Blockers**:
- Last maintained Feb 2024 (1 year ago)
- Python 3.9-3.11 only (not 3.12)
- Heavy dependency (torch, large models)
- Need to verify it still works

**Cost**: FREE (local)  
**Files Needed**:
- `providers/coqui_tts.py`
- `audio_analyzer.py` (for mouth sync)
- `mouth_sync.py` (Little Monster feature)
- Integration tests

**Implementation Notes**:
```python
from TTS.api import TTS
tts = TTS(model_name="tts_models/en/jenny/jenny")
tts.tts_to_file(text=text, file_path="output.wav")
```

**Audio Analysis for Mouth Sync**:
```python
import numpy as np
from scipy.io import wavfile

def analyze_audio_for_mouth_sync(wav_file):
    rate, audio = wavfile.read(wav_file)
    # FFT analysis for amplitude
    # Return mouth_open % over time for React animation
```

---

### Priority 2: Free Backup Providers

#### 3. edge-tts (Microsoft Edge TTS)
**Status**: Research Complete  
**Priority**: MEDIUM (Free backup)  
**Effort**: 2-3 hours

**Why**:
- HIGH quality (⭐⭐⭐⭐)
- FREE (no API key needed)
- Multiple voices
- Actively maintained

**Blockers**: None  
**Cost**: FREE  
**Files Needed**:
- `providers/edge_tts.py`
- Async implementation (edge-tts uses asyncio)

**Implementation Notes**:
```python
import edge_tts
import asyncio

async def speak(text, voice="en-US-JennyNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("output.mp3")
```

---

#### 4. pyttsx3 (Offline Fallback)
**Status**: Research Complete  
**Priority**: LOW (Emergency offline fallback)  
**Effort**: 1-2 hours

**Why**:
- Works OFFLINE
- Instant (no network latency)
- Good for demos without internet
- Very lightweight

**Blockers**: None  
**Cost**: FREE  
**Quality**: ⭐⭐ (Robotic but functional)

**Files Needed**:
- `providers/pyttsx3_tts.py`

**Implementation Notes**:
```python
import pyttsx3
engine = pyttsx3.init()
engine.save_to_file(text, 'output.wav')
engine.runAndWait()
```

---

### Priority 3: Alternative Providers (Documented, Not Prioritized)

#### 5. AWS Polly Generative Engine
**Status**: Research Complete  
**Priority**: LOW (Complex setup)  
**Effort**: 6-8 hours (AWS setup, IAM, testing)

**Why**:
- Good quality (⭐⭐⭐⭐)
- SSML customization
- FREE tier (100k first year)
- No dropped words

**Blockers**:
- Complex AWS setup (CLI, IAM, boto3)
- Region-specific (not all regions support generative)
- More effort than benefit vs Azure

**Cost**: FREE first year (100k), then $30/1M chars  
**Decision**: Skip unless Azure insufficient

---

#### 6. Google Cloud TTS
**Status**: Research Complete - **NOT RECOMMENDED**  
**Priority**: NONE  
**Effort**: N/A

**Why NOT to Implement**:
- ❌ Drops words randomly
- ❌ Blows past periods
- ❌ Unpredictable LLM behavior
- ❌ No customization for premium voices

**Research Finding**: "Even Google's demo has unnatural pronunciation"  
**Decision**: **AVOID** - Broken product

---

#### 7. ElevenLabs
**Status**: Research Complete - **NOT RECOMMENDED**  
**Priority**: NONE  
**Effort**: N/A

**Why NOT to Implement**:
- ❌ Studio crashes frequently
- ❌ Skips words, adds syllables
- ❌ You pay for mistakes
- ❌ Most expensive ($2.22-$3 per 30k vs $0.90)

**Research Finding**: "Too buggy and expensive for solo developers"  
**Decision**: **AVOID** - Not production-ready

---

## Architecture Extensions

### Multi-Provider Engine
**Status**: Designed, Not Implemented  
**Priority**: MEDIUM  
**Effort**: 4-6 hours

**Design**:
```python
class TTSEngine:
    def __init__(self, provider='azure'):
        self.provider = self._load_provider(provider)
    
    def speak(self, text, voice=None):
        return self.provider.speak(text, voice)
    
    def set_provider(self, provider_name):
        self.provider = self._load_provider(provider_name)
```

**Benefits**:
- Easy provider switching
- Fallback chain for reliability
- Test multiple providers easily

**Files Needed**:
- `tts_engine.py` (abstract base)
- `providers/base.py` (provider interface)
- Provider implementations

---

### Audio Analysis (Little Monster Feature)
**Status**: Designed, Not Implemented  
**Priority**: MEDIUM (Needed for Little Monster)  
**Effort**: 3-4 hours

**Purpose**: Generate mouth sync data for React animation

**Features Needed**:
```python
class AudioAnalyzer:
    def analyze(self, audio_file) -> AudioData
    def get_mouth_positions(self, audio_data) -> List[float]
    def get_amplitude_over_time(self, audio_data) -> np.array
```

**Output Format** (for React):
```json
{
    "timestamps": [0, 0.1, 0.2, 0.3, ...],
    "mouth_open": [0, 45, 75, 90, ...],
    "amplitude": [0, 25, 50, 30, ...]
}
```

---

### Voice Comparison Tool
**Status**: Designed, Not Implemented  
**Priority**: LOW  
**Effort**: 2-3 hours

**Purpose**: Generate same text with all providers for quality comparison

**Features**:
```python
def compare_voices(text, providers=['azure', 'openai', 'coqui']):
    for provider in providers:
        tts.set_provider(provider)
        tts.save_to_file(text, f'samples/{provider}_sample.wav')
```

---

### Chatbot Integration
**Status**: Designed, Not Implemented  
**Priority**: MEDIUM  
**Effort**: 2-3 hours

**Purpose**: Integrate TTS with POC 00 chatbot for voice responses

**Example**:
```python
# User asks question
question = "What is mitochondria?"

# Chatbot responds
answer = rag_chatbot.ask(question)

# Speak answer
tts.speak(answer)
```

---

## Dependencies Status

### Implemented:
- azure-cognitiveservices-speech ✅

### Documented for Future:
- openai (OpenAI TTS)
- TTS (Coqui TTS)
- torch (Coqui requirement)
- soundfile (Coqui requirement)
- edge-tts (Edge TTS)
- pyttsx3 (Offline TTS)
- pygame (Audio playback)
- numpy (Audio analysis)

---

## Testing Strategy

### Current Tests Needed:
- [ ] Azure TTS voice list
- [ ] Azure TTS basic generation
- [ ] Azure TTS SSML support
- [ ] Audio file output verification
- [ ] Error handling

### Future Tests (Backlog):
- [ ] Multi-provider switching
- [ ] Provider fallback chain
- [ ] Audio analysis accuracy
- [ ] Mouth sync data validation
- [ ] Cross-provider quality comparison
- [ ] Chatbot integration E2E

---

## Configuration Management

### Current:
- Environment variables for Azure
- Simple provider selection

### Future (Backlog):
```json
{
    "default_provider": "azure",
    "fallback_chain": ["azure", "openai", "edge", "pyttsx3"],
    "providers": {
        "azure": {
            "enabled": true,
            "voice": "en-US-JennyNeural"
        },
        "openai": {
            "enabled": false,
            "voice": "fable"
        }
    }
}
```

---

## Little Monster Integration Path

### Phase 1 (Current): POC 11 with Azure
- ✅ Research complete
- ✅ Azure TTS working
- ✅ Basic text-to-speech

### Phase 2 (Backlog): Audio Analysis
- Implement Coqui TTS
- Build audio analyzer
- Generate mouth sync data
- Format for React

### Phase 3 (Backlog): React Integration
- Create Flask API (like Little Monster spec)
- Return audio + mouth sync data
- React frontend consumes

---

## Documentation Backlog

### Created:
- ✅ TTS-RESEARCH-ANALYSIS.md
- ✅ POC-11-STRATEGY.md
- ✅ BACKLOG.md (this file)

### Needed:
- [ ] README.md (overview)
- [ ] START-HERE.md (quick start guide)
- [ ] API-REFERENCE.md (provider APIs)
- [ ] TROUBLESHOOTING.md (common issues)
- [ ] INTEGRATION-GUIDE.md (chatbot + Little Monster)
- [ ] POC-STATUS.md (final results)

---

## Decision Log

| Date | Decision | Reason |
|------|----------|--------|
| 2025-11-01 | Use Azure as primary | FREE 500k/month, good quality, actively maintained |
| 2025-11-01 | Defer OpenAI | Focus on free option first, add later for production |
| 2025-11-01 | Verify Coqui real | ✅ Confirmed (43k stars), but deferred due to maintenance concerns |
| 2025-11-01 | Skip Google TTS | Research shows broken product (drops words) |
| 2025-11-01 | Skip ElevenLabs | Too buggy and expensive for current needs |
| 2025-11-01 | Defer multi-provider | Build working solution first, abstract later |

---

## Cost Projection

### Development Phase (Current):
- Azure TTS: **$0/month** (FREE tier)
- **Total: $0/month** 🎉

### Production Phase (Future):
- Azure TTS: $0 for first 500k chars, then $0.90 per 30k
- OpenAI TTS: $0.90 per 30k (when added)
- Coqui TTS: $0 (local)
- **Estimated: $50-100/month** at moderate scale

### Scaling Strategy:
1. Use Azure FREE tier (500k chars/month)
2. Add Coqui for overflow (local, free)
3. Add OpenAI for premium quality
4. Add edge-tts for additional free capacity

---

## Success Metrics

### POC 11 Complete (Current Sprint):
- [x] Research completed
- [x] Strategy documented
- [x] Backlog created
- [ ] Azure TTS working
- [ ] CLI tool functional
- [ ] Basic tests passing
- [ ] Documentation complete

### Future Milestones:
- [ ] OpenAI provider added
- [ ] Coqui + audio analysis working
- [ ] Multi-provider engine complete
- [ ] Little Monster integration ready
- [ ] Chatbot voice responses working

---

## Timeline Estimates

| Item | Effort | Priority | Status |
|------|--------|----------|--------|
| Azure TTS | 2-3h | HIGH | IN PROGRESS |
| CLI Tool | 1h | HIGH | NEXT |
| Documentation | 1h | HIGH | NEXT |
| OpenAI Provider | 2-3h | HIGH | BACKLOG |
| Coqui + Analysis | 4-6h | MEDIUM | BACKLOG |
| edge-tts | 2-3h | MEDIUM | BACKLOG |
| Multi-provider | 4-6h | MEDIUM | BACKLOG |
| Chatbot Integration | 2-3h | MEDIUM | BACKLOG |
| Little Monster | 3-4h | MEDIUM | BACKLOG |

**Total Backlog Effort**: 18-28 hours

---

## Notes

- Research stored in Chroma: `ai_ml_comprehensive_docs` collection
- All research findings in `TTS-RESEARCH-ANALYSIS.md`
- Strategy and architecture in `POC-11-STRATEGY.md`
- Focus on pragmatic implementation: Azure first, expand later
- Avoid premature abstraction - build working solution first

---

Last Updated: 2025-11-01
