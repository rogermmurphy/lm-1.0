from TTS.api import TTS
import time

tests = {
    "Short": "Hello, world!",
    "Medium": "The quick brown fox jumps over the lazy dog. This is a test of Azure Text-to-Speech with a medium-length sentence.",
    "Long": "Artificial intelligence is transforming the way we interact with technology. From voice assistants to automated customer service, text-to-speech technology has become an essential part of modern applications. Azure's Speech Services provide high-quality, natural-sounding voices that can enhance user experience across a wide range of applications.",
    "Very Long": "The history of artificial intelligence dates back to ancient times, with myths and stories of artificial beings endowed with intelligence. The field of AI research was founded at a workshop at Dartmouth College in 1956. Since then, the field has experienced several waves of optimism, followed by disappointment and criticism, followed by funding cuts. In recent years, advances in machine learning have led to a resurgence in AI research and applications. Today, artificial intelligence powers everything from recommendation systems to autonomous vehicles, and text-to-speech technology represents just one of many practical applications of this revolutionary field. The future of AI promises even more remarkable innovations that will continue to reshape how we live and work."
}

print("Coqui TTS Benchmark")
print("=" * 50)
tts = TTS(model_name='tts_models/en/jenny/jenny', progress_bar=False, gpu=False)

for name, text in tests.items():
    print(f"\n{name} ({len(text)} chars)")
    start = time.time()
    tts.tts_to_file(text=text, file_path=f'/output/coqui_{name.lower()}.wav')
    gen_time = time.time() - start
    print(f"Time: {gen_time:.3f}s")
