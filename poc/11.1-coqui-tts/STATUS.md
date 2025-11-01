# POC 11.1: Coqui TTS Status

## Current Status: Model Download Complete, Processing...

### Progress
- [x] Docker image pulled (ghcr.io/coqui-ai/tts-cpu)
- [x] Container started successfully
- [x] Jenny model downloaded (1.61 GB, 100%)
- [ ] Audio generation in progress...
- [ ] Waiting for coqui_test.wav output

### Timeline
- Docker pull: ~3 minutes
- Model download: ~2 minutes (1.61 GB)
- Audio generation: Expected 30-60 seconds (first run)
- Total time: ~5-6 minutes for first run

### What's Happening
The Coqui TTS container has:
1. Downloaded the Docker image
2. Downloaded the Jenny voice model (1.61 GB)
3. Currently processing the text and generating audio

### Next Steps (When Complete)
1. Verify coqui_test.wav created
2. Play audio to hear Coqui voice
3. Compare with Azure audio quality
4. Run full benchmarks on both
5. Present objective comparison

### Expected Behavior
Once generation completes:
- File: coqui_test.wav will appear in poc/11.1-coqui-tts/
- Container will exit automatically (--rm flag)
- Can then run benchmarks for performance comparison

### Commands Ready for After Generation

**Play Coqui Audio:**
```bash
cd poc/11.1-coqui-tts
start coqui_test.wav
```

**Run Full Benchmark:**
```bash
docker run --rm -v %cd%:/output --entrypoint python3 ghcr.io/coqui-ai/tts-cpu /output/benchmark_coqui.py
```

### Why So Slow First Time?
- Model download: 1.61 GB (one-time)
- Model loading into memory
- Audio generation
- Subsequent runs will be MUCH faster (model cached)

### Comparison Preview

**Azure TTS** (Already Measured):
- Generation: 0.8-0.9s
- Speed: 7x real-time
- No model download needed

**Coqui TTS** (In Progress):
- Model download: 1.61 GB (one-time)
- First generation: ~30-60s (loading model)
- Subsequent: Expected 2-10s (model cached)
- Local execution (no API calls)
