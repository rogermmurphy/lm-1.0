# POC 11.1: Coqui TTS Docker Implementation

## Setup Using Docker

Coqui TTS requires C++ compilation on Windows. Docker bypasses this issue.

### Quick Start

```bash
# 1. Pull Docker image (one-time, ~2GB download)
docker pull ghcr.io/coqui-ai/tts-cpu

# 2. Run test
run_coqui_docker.bat

# 3. Audio will be in output/coqui_test.wav
```

## Implementation Files

- `coqui_tts.py` - Coqui TTS wrapper (Jenny model)
- `benchmark_coqui.py` - Performance testing
- `Dockerfile` - Custom Docker setup
- `run_coqui_docker.bat` - Quick test script

## Coqui TTS Features

### Models
- tts_models/en/jenny/jenny (Little Monster spec)
- XTTS v2 (16 languages, voice cloning)
- 1100+ language models via Fairseq
- Bark (expressive, nonverbal sounds)
- YourTTS (multi-lingual voice cloning)

### Capabilities
- Local execution (no API calls)
- Voice cloning from audio sample
- Offline operation
- Custom model training
- Open source (MPL-2.0)

## Docker vs Native Installation

### Native Install (Windows)
- Requires: Visual C++ Build Tools (6-8 GB)
- Time: 30-60 minutes
- Result: Failed on our system

### Docker Install
- Requires: Docker Desktop
- Time: 5-10 minutes (image download)
- Result: Working

## Usage

### In Docker Container

```bash
docker run --rm -v %cd%\output:/app/output ghcr.io/coqui-ai/tts-cpu python3 -c "
from TTS.api import TTS
tts = TTS('tts_models/en/jenny/jenny', gpu=False)
tts.tts_to_file('Your text here', '/app/output/output.wav')
"
```

### Python API (in container)

```python
from TTS.api import TTS

# Initialize
tts = TTS(model_name="tts_models/en/jenny/jenny", gpu=False)

# Generate speech
tts.tts_to_file(
    text="Your text here",
    file_path="output.wav"
)
```

## Benchmark Tests

Same test data as Azure for fair comparison:
- Short: 13 characters
- Medium: 114 characters
- Long: 402 characters
- Very Long: 877 characters

## Notes

- First run downloads Jenny model (~100MB)
- Subsequent runs use cached model
- Audio files saved to output/ directory
- Performance measured with same methodology as Azure
