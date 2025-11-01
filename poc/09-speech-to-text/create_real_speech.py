#!/usr/bin/env python3
"""
Create Real Speech Audio - Generate MP3 with actual spoken words
"""

from gtts import gTTS

# Biology lecture text
text = """Hello and welcome to today's biology lecture. 
Today we will discuss the structure and function of cells. 
Cells are the basic building blocks of all living organisms. 
Inside the cell we find the nucleus which contains genetic material. 
The mitochondria are often called the powerhouse of the cell. 
They generate energy through cellular respiration. 
The cell membrane controls what enters and exits the cell. 
This concludes our brief introduction to cell biology."""

print("Creating audio file with real speech...")
tts = gTTS(text=text, lang='en', slow=False)
tts.save('real_lecture.mp3')

import os
size_mb = os.path.getsize('real_lecture.mp3') / (1024 * 1024)
print(f"[OK] Created: real_lecture.mp3 ({size_mb:.2f} MB)")
print(f"[OK] This file contains ACTUAL SPEECH about biology")
print("\nExpected transcript:")
print("-" * 70)
print(text)
print("-" * 70)
