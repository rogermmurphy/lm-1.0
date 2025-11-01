@echo off
REM POC 11.1: Run Coqui TTS in Docker
REM This script runs the benchmark tests and copies audio files out

echo ============================================================
echo POC 11.1: Running Coqui TTS Benchmark in Docker
echo ============================================================

REM Create output directory for audio files
if not exist "output" mkdir output

echo.
echo [INFO] Running Coqui TTS benchmark...
echo.

REM Run Docker container with volume mount to get audio files out
docker run --rm -v %cd%\output:/app/output ghcr.io/coqui-ai/tts-cpu python3 -c "from TTS.api import TTS; import time; tts = TTS(model_name='tts_models/en/jenny/jenny', progress_bar=False, gpu=False); print('[SUCCESS] Coqui TTS loaded'); text='Hello! This is a test of Coqui TTS using the Jenny voice model.'; start=time.time(); tts.tts_to_file(text=text, file_path='/app/output/coqui_test.wav'); gen_time=time.time()-start; print(f'[SUCCESS] Generated in {gen_time:.3f}s'); print(f'[INFO] Characters: {len(text)}')"

echo.
echo ============================================================
echo [SUCCESS] Coqui TTS test complete!
echo ============================================================
echo.
echo Audio file saved to: output\coqui_test.wav
echo.
echo Play it with: start output\coqui_test.wav
echo.

pause
