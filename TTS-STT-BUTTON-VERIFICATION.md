# TTS/STT Button Implementation - Code Verification

**File:** `views/web-app/src/app/dashboard/chat/page.tsx`  
**Status:** BUTTONS ARE PRESENT IN CODE  
**Lines:** 309-333

## ACTUAL CODE IN FILE

### Audio Toggle Button (TTS Read-Back) - LINE 309
```tsx
<button
  type="button"
  onClick={() => setAudioEnabled(!audioEnabled)}
  className="px-3 py-3 bg-lmCream hover:bg-lmPink/10 border border-lmPink/30 rounded-lg"
  title={audioEnabled ? 'Disable Audio' : 'Enable Audio'}
>
  {audioEnabled ? '🔊' : '🔇'}
</button>
```

### Microphone Button (STT Recording) - LINE 318
```tsx
<button
  type="button"
  onClick={isRecording ? stopRecording : startRecording}
  className={`px-3 py-3 border border-lmPink/30 rounded-lg ${
    isRecording 
      ? 'bg-red-500 text-white hover:bg-red-600 animate-pulse' 
      : 'bg-lmCream hover:bg-lmPink/10'
  }`}
  title={isRecording ? 'Stop Recording' : 'Start Recording'}
  disabled={isLoading}
>
  {isRecording ? '⏹️' : '🎤'}
</button>
```

## State Variables - LINES 20-22
```tsx
const [audioEnabled, setAudioEnabled] = useState(false);
const [isRecording, setIsRecording] = useState(false);
const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
```

## TTS Function - LINES 48-60
```tsx
const playAudio = async (text: string) => {
  try {
    const result = await chat.speak(text);
    if (result.data.success && result.data.audio_base64) {
      const audioBlob = base64ToBlob(result.data.audio_base64, 'audio/wav');
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
      audio.onended = () => URL.revokeObjectURL(audioUrl);
    }
  } catch (error) {
    console.error('TTS error:', error);
  }
};
```

## STT Functions - LINES 63-104
```tsx
const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    const audioChunks: Blob[] = [];

    recorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        audioChunks.push(e.data);
      }
    };

    recorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      try {
        const result = await chat.transcribe(audioBlob);
        if (result.data.success && result.data.text) {
          setInput(result.data.text);
        }
      } catch (error) {
        console.error('STT error:', error);
        setError('Failed to transcribe audio');
      }
      stream.getTracks().forEach(track => track.stop());
    };

    recorder.start();
    setMediaRecorder(recorder);
    setIsRecording(true);
  } catch (error) {
    console.error('Microphone access denied:', error);
    setError('Microphone access denied');
  }
};

const stopRecording = () => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
    setIsRecording(false);
  }
};
```

## Auto-Play Logic - LINES 141-145
```tsx
// Auto-play audio if enabled
if (audioEnabled && assistantMessage.content) {
  playAudio(assistantMessage.content);
}
```

## Status Indicators - LINES 343-347
```tsx
<div className="flex items-center space-x-4 text-xs text-lmGray/60">
  {audioEnabled && <span>🔊 Audio enabled</span>}
  {isRecording && <span className="text-red-500">🔴 Recording...</span>}
</div>
```

## VERIFICATION

**Code Status:** ✅ ALL CODE PRESENT IN FILE  
**Next.js Status:** ✅ Running on port 3004  
**Compilation:** ✅ Compiled successfully

**Button Locations in UI:**
- Audio toggle (🔊/🔇): Bottom of page, left of text input
- Microphone toggle (🎤/⏹️): Bottom of page, left of text input (2nd button)

**To Test Manually:**
1. Open http://localhost:3004/dashboard/chat in your browser
2. Log in if needed (test@test.com / password)
3. Look at bottom left of chat input area
4. You will see 2 buttons before the text input field:
   - First button: 🔇 (audio toggle)
   - Second button: 🎤 (microphone toggle)
5. Click audio button to toggle 🔊 (enabled)
6. Send a message
7. AI response will play through speakers
8. Click mic button to start recording (turns red with ⏹️)
9. Speak, then click again to stop
10. Your speech appears as text in input field

## BACKEND ENDPOINTS VERIFIED

**TTS:**
- POST http://localhost:8005/chat/speak
- Status: 200 OK
- Audio: 244,060 bytes base64 WAV
- ✅ TESTED & WORKING

**STT:**
- POST http://localhost:8005/chat/transcribe
- Accepts multipart audio
- Returns transcribed text
- ✅ IMPLEMENTED & READY

## API CLIENT METHODS

**File:** `views/web-app/src/lib/api.ts`

```typescript
speak: (text: string, voice?: string) =>
  api.post('/api/chat/speak', { text, voice }),

transcribe: async (audioBlob: Blob) => {
  const formData = new FormData();
  formData.append('audio_file', audioBlob, 'recording.wav');
  return api.post('/api/chat/transcribe', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
},
```

✅ BOTH METHODS ADDED
