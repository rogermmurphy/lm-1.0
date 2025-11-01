import requests
import time

# Coqui server endpoint
url = "http://localhost:5002/api/tts"

tests = [
    ("test_basic", "Hello! This is a test of Coqui Text-to-Speech. How do I sound?"),
    ("test_guy", "This is another voice test."),
    ("test_ssml", "This is very important information. Please listen carefully."),
    ("benchmark_short", "Hello, world!"),
    ("benchmark_medium", "The quick brown fox jumps over the lazy dog. This is a test of Azure Text-to-Speech with a medium-length sentence."),
    ("benchmark_long", "Artificial intelligence is transforming the way we interact with technology. From voice assistants to automated customer service, text-to-speech technology has become an essential part of modern applications. Azure's Speech Services provide high-quality, natural-sounding voices that can enhance user experience across a wide range of applications."),
    ("benchmark_very_long", "The history of artificial intelligence dates back to ancient times, with myths and stories of artificial beings endowed with intelligence. The field of AI research was founded at a workshop at Dartmouth College in 1956. Since then, the field has experienced several waves of optimism, followed by disappointment and criticism, followed by funding cuts. In recent years, advances in machine learning have led to a resurgence in AI research and applications. Today, artificial intelligence powers everything from recommendation systems to autonomous vehicles, and text-to-speech technology represents just one of many practical applications of this revolutionary field. The future of AI promises even more remarkable innovations that will continue to reshape how we live and work.")
]

print("Coqui TTS Benchmark (via HTTP server)")
print("=" * 60)

for name, text in tests:
    print(f"\n{name}: {len(text)} chars")
    start = time.time()
    response = requests.get(url, params={"text": text})
    gen_time = time.time() - start
    
    if response.status_code == 200:
        with open(f"coqui_{name}.wav", "wb") as f:
            f.write(response.content)
        print(f"Time: {gen_time:.3f}s")
    else:
        print(f"Error: {response.status_code}")

print("\n" + "=" * 60)
print("Complete")
