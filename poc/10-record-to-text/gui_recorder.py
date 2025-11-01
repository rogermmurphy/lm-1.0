"""
POC 10: GUI Audio Recorder
Tkinter-based graphical interface for recording audio
Click button to start/stop recording
"""
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import threading
from audio_recorder import AudioRecorder

# Add POC 09 to path for transcription integration
sys.path.insert(0, str(Path(__file__).parent.parent / '09-speech-to-text'))

try:
    from async_transcription_tool import AsyncTranscriptionTool
    POC09_AVAILABLE = True
except ImportError:
    POC09_AVAILABLE = False


class RecorderGUI:
    """GUI application for audio recording"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("POC 10: Record-to-Text")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Initialize recorder
        self.recorder = AudioRecorder(
            sample_rate=16000,
            channels=1,
            dtype='int16'
        )
        
        self.is_recording = False
        self.audio_data = None
        self.update_timer = None
        
        self.create_widgets()
        self.check_microphone()
    
    def create_widgets(self):
        """Create GUI widgets"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🎤 Record-to-Text",
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=15)
        
        # Main content frame
        content_frame = tk.Frame(self.root, padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Status indicator
        self.status_frame = tk.Frame(content_frame)
        self.status_frame.pack(pady=10)
        
        self.status_indicator = tk.Canvas(
            self.status_frame,
            width=20,
            height=20,
            bg='white',
            highlightthickness=0
        )
        self.status_indicator.pack(side='left', padx=5)
        self.status_circle = self.status_indicator.create_oval(
            2, 2, 18, 18,
            fill='gray',
            outline=''
        )
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            font=('Arial', 12)
        )
        self.status_label.pack(side='left')
        
        # Duration display
        self.duration_label = tk.Label(
            content_frame,
            text="0:00",
            font=('Arial', 32, 'bold'),
            fg='#34495e'
        )
        self.duration_label.pack(pady=20)
        
        # Record button
        self.record_button = tk.Button(
            content_frame,
            text="⏺ Start Recording",
            font=('Arial', 14, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            width=20,
            height=2,
            command=self.toggle_recording,
            cursor='hand2'
        )
        self.record_button.pack(pady=10)
        
        # Device info
        device_frame = tk.LabelFrame(
            content_frame,
            text="Microphone",
            font=('Arial', 10),
            padx=10,
            pady=10
        )
        device_frame.pack(fill='x', pady=10)
        
        self.device_label = tk.Label(
            device_frame,
            text="Checking...",
            font=('Arial', 9),
            fg='#7f8c8d',
            wraplength=450,
            justify='left'
        )
        self.device_label.pack()
        
        # Info text
        info_text = "Click 'Start Recording' to begin.\nSpeak into your microphone.\nClick 'Stop Recording' when done."
        if POC09_AVAILABLE:
            info_text += "\n\n✅ Auto-transcription enabled (POC 09)"
        else:
            info_text += "\n\n⚠️ POC 09 not available - transcription disabled"
        
        info_label = tk.Label(
            content_frame,
            text=info_text,
            font=('Arial', 9),
            fg='#95a5a6',
            justify='center'
        )
        info_label.pack(pady=10)
    
    def check_microphone(self):
        """Check for available microphone"""
        try:
            device = self.recorder.get_default_device()
            self.device_label.config(
                text=f"✓ {device['name']}\n"
                     f"Sample Rate: {device['default_samplerate']:.0f} Hz"
            )
        except Exception as e:
            self.device_label.config(
                text=f"❌ Error: {str(e)}",
                fg='red'
            )
            messagebox.showerror(
                "Microphone Error",
                "Could not detect microphone.\nPlease check your audio settings."
            )
    
    def toggle_recording(self):
        """Start or stop recording"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording audio"""
        try:
            self.is_recording = True
            self.recorder.start_recording()
            
            # Update UI
            self.record_button.config(
                text="⏹ Stop Recording",
                bg='#e74c3c',
                activebackground='#c0392b'
            )
            self.status_label.config(text="Recording...")
            self.status_indicator.itemconfig(self.status_circle, fill='red')
            
            # Start duration update timer
            self.update_duration()
            
        except Exception as e:
            self.is_recording = False
            messagebox.showerror("Recording Error", str(e))
    
    def stop_recording(self):
        """Stop recording and save audio"""
        try:
            # Stop recording
            self.audio_data = self.recorder.stop_recording()
            self.is_recording = False
            
            # Cancel duration timer
            if self.update_timer:
                self.root.after_cancel(self.update_timer)
                self.update_timer = None
            
            # Update UI
            self.record_button.config(
                text="⏺ Start Recording",
                bg='#27ae60',
                activebackground='#229954'
            )
            self.status_label.config(text="Processing...")
            self.status_indicator.itemconfig(self.status_circle, fill='orange')
            
            if self.audio_data is not None:
                # Save in separate thread to avoid blocking UI
                threading.Thread(
                    target=self.save_and_transcribe,
                    daemon=True
                ).start()
            else:
                self.status_label.config(text="Ready")
                self.status_indicator.itemconfig(self.status_circle, fill='gray')
                messagebox.showwarning("No Audio", "No audio was recorded.")
            
        except Exception as e:
            self.is_recording = False
            messagebox.showerror("Error", str(e))
    
    def save_and_transcribe(self):
        """Save audio file and queue for transcription"""
        try:
            # Save to file
            recordings_dir = Path(__file__).parent / "recordings"
            filepath = self.recorder.save_to_file(
                self.audio_data,
                output_dir=str(recordings_dir)
            )
            
            duration = len(self.audio_data) / self.recorder.sample_rate
            file_size = Path(filepath).stat().st_size / 1024  # KB
            
            message = f"Recording saved!\n\n"
            message += f"Duration: {duration:.2f} seconds\n"
            message += f"Size: {file_size:.1f} KB\n"
            message += f"File: {Path(filepath).name}\n"
            
            # Queue for transcription if available
            if POC09_AVAILABLE:
                try:
                    tool = AsyncTranscriptionTool()
                    result = tool.transcribe_audio_async(
                        file_path=filepath,
                        user_id='gui_user',
                        subject='voice_recording',
                        auto_load_to_chromadb=True
                    )
                    
                    if result['status'] == 'queued':
                        message += f"\n✅ Queued for transcription\n"
                        message += f"Job ID: {result['job_id']}"
                    else:
                        message += f"\n⚠️ Status: {result['status']}"
                        
                except Exception as e:
                    message += f"\n⚠️ Transcription error:\n{str(e)}"
            else:
                message += "\n💡 POC 09 not available\n"
                message += "Manual transcription needed"
            
            # Update UI in main thread
            self.root.after(0, lambda: self.show_success(message))
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))
    
    def show_success(self, message):
        """Show success message and reset UI"""
        self.status_label.config(text="Ready")
        self.status_indicator.itemconfig(self.status_circle, fill='green')
        messagebox.showinfo("Success", message)
        
        # Reset after showing message
        self.root.after(1000, self.reset_ui)
    
    def show_error(self, error):
        """Show error message"""
        self.status_label.config(text="Error")
        self.status_indicator.itemconfig(self.status_circle, fill='red')
        messagebox.showerror("Error", error)
        self.reset_ui()
    
    def reset_ui(self):
        """Reset UI to initial state"""
        self.duration_label.config(text="0:00")
        self.status_label.config(text="Ready")
        self.status_indicator.itemconfig(self.status_circle, fill='gray')
    
    def update_duration(self):
        """Update duration display during recording"""
        if self.is_recording:
            duration = self.recorder.get_duration()
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            self.duration_label.config(text=f"{minutes}:{seconds:02d}")
            
            # Schedule next update
            self.update_timer = self.root.after(100, self.update_duration)


def main():
    """Launch the GUI application"""
    root = tk.Tk()
    app = RecorderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
