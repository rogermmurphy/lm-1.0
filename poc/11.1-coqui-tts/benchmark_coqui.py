"""
POC 11.1: Coqui TTS Benchmark
Performance comparison with same test data as Azure
"""

import time
import wave
from coqui_tts import CoquiTTS


def get_audio_duration(wav_file):
    """Get duration of wav file in seconds."""
    with wave.open(wav_file, 'r') as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        duration = frames / float(rate)
        return duration


def benchmark_coqui(text_samples):
    """
    Benchmark Coqui TTS with same tests as Azure.
    """
    print("=" * 70)
    print("POC 11.1: Coqui TTS Performance Benchmark")
    print("=" * 70)
    
    # Initialize TTS
    tts = CoquiTTS()
    print(f"\n[INFO] Model: {tts.model_name}")
    print(f"[INFO] GPU: {tts.gpu}")
    
    results = []
    
    for i, (name, text) in enumerate(text_samples.items(), 1):
        print(f"\n{'=' * 70}")
        print(f"Test {i}: {name}")
        print(f"{'=' * 70}")
        print(f"Text length: {len(text)} characters")
        print(f"Text preview: {text[:80]}{'...' if len(text) > 80 else ''}")
        
        output_file = f"coqui_benchmark_{name.replace(' ', '_').lower()}.wav"
        
        # Measure generation time
        start_time = time.time()
        success = tts.speak(text, output_file)
        generation_time = time.time() - start_time
        
        if success:
            # Get audio duration
            audio_duration = get_audio_duration(output_file)
            
            # Calculate metrics
            chars_per_sec = len(text) / generation_time
            rtf = generation_time / audio_duration
            
            result = {
                'name': name,
                'chars': len(text),
                'gen_time': generation_time,
                'audio_duration': audio_duration,
                'chars_per_sec': chars_per_sec,
                'rtf': rtf
            }
            results.append(result)
            
            print(f"\n[METRICS]")
            print(f"  Generation time: {generation_time:.3f} seconds")
            print(f"  Audio duration: {audio_duration:.3f} seconds")
            print(f"  Chars/second: {chars_per_sec:.1f}")
            print(f"  Real-Time Factor: {rtf:.3f}x")
            
            if rtf < 1.0:
                speedup = 1.0 / rtf
                print(f"  Speed: {speedup:.1f}x faster than real-time")
            else:
                print(f"  Speed: {rtf:.1f}x slower than real-time")
        else:
            print(f"\n[ERROR] Failed to generate audio")
    
    # Summary
    print(f"\n{'=' * 70}")
    print("COQUI TTS BENCHMARK SUMMARY")
    print(f"{'=' * 70}")
    
    if results:
        print(f"\n{'Test':<20} {'Chars':<8} {'Gen(s)':<8} {'Audio(s)':<8} {'RTF':<8} {'Speed'}")
        print("-" * 70)
        
        for r in results:
            speedup = 1.0 / r['rtf'] if r['rtf'] < 1.0 else r['rtf']
            speed_str = f"{speedup:.1f}x {'faster' if r['rtf'] < 1.0 else 'slower'}"
            print(f"{r['name']:<20} {r['chars']:<8} {r['gen_time']:<8.3f} "
                  f"{r['audio_duration']:<8.3f} {r['rtf']:<8.3f} {speed_str}")
        
        # Averages
        avg_rtf = sum(r['rtf'] for r in results) / len(results)
        avg_chars_per_sec = sum(r['chars_per_sec'] for r in results) / len(results)
        
        print("-" * 70)
        print(f"{'AVERAGE':<20} {'':<8} {'':<8} {'':<8} {avg_rtf:<8.3f}")
        print(f"\nAverage throughput: {avg_chars_per_sec:.1f} characters/second")
        
        if avg_rtf < 1.0:
            print(f"Overall speed: {1.0/avg_rtf:.1f}x faster than real-time")
        else:
            print(f"Overall speed: {avg_rtf:.1f}x slower than real-time")
        
        # Cost
        total_chars = sum(r['chars'] for r in results)
        print(f"\n[COST]")
        print(f"  Total characters: {total_chars}")
        print(f"  Cost: $0 (local execution)")


if __name__ == "__main__":
    # Same samples as Azure benchmark for fair comparison
    samples = {
        "Short": "Hello, world!",
        
        "Medium": "The quick brown fox jumps over the lazy dog. This is a test of Azure Text-to-Speech with a medium-length sentence.",
        
        "Long": """
        Artificial intelligence is transforming the way we interact with technology. 
        From voice assistants to automated customer service, text-to-speech technology 
        has become an essential part of modern applications. Azure's Speech Services 
        provide high-quality, natural-sounding voices that can enhance user experience 
        across a wide range of applications.
        """,
        
        "Very Long": """
        The history of artificial intelligence dates back to ancient times, with myths 
        and stories of artificial beings endowed with intelligence. The field of AI research 
        was founded at a workshop at Dartmouth College in 1956. Since then, the field has 
        experienced several waves of optimism, followed by disappointment and criticism, 
        followed by funding cuts. In recent years, advances in machine learning have led 
        to a resurgence in AI research and applications. Today, artificial intelligence 
        powers everything from recommendation systems to autonomous vehicles, and text-to-speech 
        technology represents just one of many practical applications of this revolutionary 
        field. The future of AI promises even more remarkable innovations that will continue 
        to reshape how we live and work.
        """
    }
    
    benchmark_coqui(samples)
    
    print(f"\n{'=' * 70}")
    print("[SUCCESS] Coqui TTS Benchmark complete!")
    print(f"{'=' * 70}")
    print("\nGenerated benchmark audio files:")
    print("  - coqui_benchmark_short.wav")
    print("  - coqui_benchmark_medium.wav")
    print("  - coqui_benchmark_long.wav")
    print("  - coqui_benchmark_very_long.wav")
