from TTS.api import TTS
import time

print('Initializing Coqui TTS...')
tts = TTS(model_name='tts_models/en/jenny/jenny', progress_bar=False, gpu=False)
print('[SUCCESS] Loaded Jenny model')

text = 'Hello! This is Coqui TTS using the Jenny voice model.'
print(f'[INFO] Generating speech for {len(text)} characters...')

start = time.time()
tts.tts_to_file(text=text, file_path='/workspace/coqui_test.wav')
gen_time = time.time() - start

print(f'[SUCCESS] Generated in {gen_time:.3f}s')
print(f'[INFO] Characters: {len(text)}')
print(f'[INFO] Throughput: {len(text)/gen_time:.1f} chars/sec')
