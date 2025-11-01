#!/usr/bin/env python3
"""
Create Sample Audio - Generates a test audio file for transcription testing
"""

import os
import sys

def create_sample_with_gtts():
    """Create sample audio using gTTS (Google Text-to-Speech)"""
    try:
        from gtts import gTTS
        
        # Sample text about biology (fitting for a lecture)
        text = """
        Hello and welcome to today's biology lecture. 
        Today we will discuss the structure and function of cells.
        Cells are the basic building blocks of all living organisms.
        Inside the cell, we find the nucleus, which contains genetic material.
        The mitochondria are often called the powerhouse of the cell.
        They generate energy through cellular respiration.
        The cell membrane controls what enters and exits the cell.
        This concludes our brief introduction to cell biology.
        """
        
        print("Creating sample audio file using Google Text-to-Speech...")
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save('sample_lecture.mp3')
        print("[OK] Created: sample_lecture.mp3")
        return True
        
    except ImportError:
        print("[INFO] gTTS not installed. Install with: pip install gtts")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to create audio with gTTS: {e}")
        return False

def create_sample_with_pyttsx3():
    """Create sample audio using pyttsx3 (offline TTS)"""
    try:
        import pyttsx3
        
        text = """
        Hello and welcome to today's biology lecture. 
        Today we will discuss cells and their functions.
        Cells are the basic units of life.
        The nucleus contains DNA and controls cell activities.
        Mitochondria produce energy for the cell.
        """
        
        print("Creating sample audio file using pyttsx3...")
        engine = pyttsx3.init()
        engine.save_to_file(text, 'sample_lecture.mp3')
        engine.runAndWait()
        print("[OK] Created: sample_lecture.mp3")
        return True
        
    except ImportError:
        print("[INFO] pyttsx3 not installed. Install with: pip install pyttsx3")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to create audio with pyttsx3: {e}")
        return False

def download_sample_audio():
    """Download a sample audio file from the internet"""
    try:
        import urllib.request
        
        # This is a public domain audio file from archive.org
        url = "https://archive.org/download/Greatest_Speeches_of_the_20th_Century/KeynoteAddress.mp3"
        
        print("Downloading sample audio file...")
        print(f"URL: {url}")
        
        urllib.request.urlretrieve(url, 'sample_lecture.mp3')
        
        # Check file size
        size_mb = os.path.getsize('sample_lecture.mp3') / (1024 * 1024)
        print(f"[OK] Downloaded: sample_lecture.mp3 ({size_mb:.2f} MB)")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to download: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("CREATE SAMPLE AUDIO FOR TESTING")
    print("="*70 + "\n")
    
    if os.path.exists('sample_lecture.mp3'):
        print("[INFO] sample_lecture.mp3 already exists")
        size_mb = os.path.getsize('sample_lecture.mp3') / (1024 * 1024)
        print(f"[INFO] Size: {size_mb:.2f} MB")
        
        response = input("\nOverwrite existing file? (y/n): ")
        if response.lower() != 'y':
            print("Keeping existing file.")
            return
    
    print("\nChoose method to create sample audio:")
    print("1. Generate using gTTS (Google Text-to-Speech, requires internet)")
    print("2. Generate using pyttsx3 (Offline TTS)")
    print("3. Download sample from archive.org (Public domain speech)")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    success = False
    
    if choice == '1':
        success = create_sample_with_gtts()
    elif choice == '2':
        success = create_sample_with_pyttsx3()
    elif choice == '3':
        success = download_sample_audio()
    elif choice == '4':
        print("Exiting.")
        return
    else:
        print("Invalid choice.")
        return
    
    if success:
        print("\n" + "="*70)
        print("SUCCESS")
        print("="*70)
        print("\nSample audio file created!")
        print("File: sample_lecture.mp3")
        print("\nNext steps:")
        print("1. Run: python setup_and_test.py")
        print("2. Start worker: python transcription_worker.py")
        print("\n")
    else:
        print("\n" + "="*70)
        print("ALTERNATIVE: MANUAL DOWNLOAD")
        print("="*70)
        print("\nYou can manually download a sample audio file:")
        print("1. Find any MP3 or WAV file")
        print("2. Copy it to this directory")
        print("3. Rename it to: sample_lecture.mp3")
        print("\nOr install dependencies:")
        print("  pip install gtts")
        print("  pip install pyttsx3")

if __name__ == "__main__":
    main()
