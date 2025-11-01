"""
POC 11: Azure TTS Benchmark
Measure speech generation speed and performance metrics.
"""

import time
import os
from pathlib import Path
from azure_tts import AzureTTS


def get_audio_duration(wav_file):
    """Get duration of wav file in seconds."""
    import wave
    with wave.open(wav_file, 'r') as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        duration = frames / float(rate)
        return duration


def benchmark_tts(text_samples):
    """
    Benchmark Azure TTS with different text lengths.
    
    Metrics:
    - Generation time (seconds)
    - Characters per second
    - Real-time factor (RTF) - generation time / audio duration
      RTF < 1.0 means faster than real-time
    """
    print("=" * 70)
    print("POC 11: Azure TTS Performance Benchmark")
    print("=" * 70)
    
    # Initialize TTS
    tts = AzureTTS()
    print(f"\n[INFO] Testing with voice: {tts.voice}")
    print(f"[INFO] Region: {tts.region}")
    
    results = []
    
    for i, (name, text) in enumerate(text_samples.items(), 1):
        print(f"\n{'=' * 70}")
        print(f"Test {i}: {name}")
        print(f"{'=' * 70}")
        print(f"Text length: {len(text)} characters")
        print(f"Text preview: {text[:80]}{'...' if len(text) > 80 else ''}")
        
        output_file = f"benchmark_{name.replace(' ', '_').lower()}.wav"
        
        # Measure generation time
        start_time = time.time()
        success = tts.speak(text, output_file)
        generation_time = time.time() - start_time
        
        if success:
            # Get audio duration
            audio_duration = get_audio_duration(output_file)
            
            # Calculate metrics
            chars_per_sec = len(text) / generation_time
            rtf = generation_time / audio_duration  # Real-Time Factor
            
            # Store results
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
                print(f"  Speed: {speedup:.1f}x faster than real-time!")
            else:
                print(f"  Speed: {rtf:.1f}x slower than real-time")
        else:
            print(f"\n[ERROR] Failed to generate audio")
    
    # Summary
    print(f"\n{'=' * 70}")
    print("BENCHMARK SUMMARY")
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
        
        # Cost estimation
        total_chars = sum(r['chars'] for r in results)
        print(f"\n[COST]")
        print(f"  Total characters: {total_chars}")
        print(f"  Cost: $0 (FREE tier: 500,000 chars/month)")
        print(f"  Remaining free: {500000 - total_chars:,} characters")


if __name__ == "__main__":
    # Test samples of varying lengths
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
    
    benchmark_tts(samples)
    
    print(f"\n{'=' * 70}")
    print("[SUCCESS] Benchmark complete!")
    print(f"{'=' * 70}")
    print("\nGenerated benchmark audio files:")
    print("  - benchmark_short.wav")
    print("  - benchmark_medium.wav")
    print("  - benchmark_long.wav")
    print("  - benchmark_very_long.wav")
    print("\nPlay them to hear the quality!")
