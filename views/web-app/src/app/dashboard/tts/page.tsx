'use client';

import { useState, useRef } from 'react';
import { tts } from '@/lib/api';

export default function TTSPage() {
  const [text, setText] = useState('');
  const [voice, setVoice] = useState('en-US-AvaMultilingualNeural');
  const [isGenerating, setIsGenerating] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [error, setError] = useState('');
  const audioRef = useRef<HTMLAudioElement>(null);

  const handleGenerate = async () => {
    if (!text.trim()) return;

    setIsGenerating(true);
    setError('');
    setAudioUrl(null);

    try {
      const response = await tts.generate(text, voice);
      
      // Convert base64 audio to blob URL
      const audioData = response.data.audio_base64 || response.data.audio;
      if (audioData) {
        const blob = base64ToBlob(audioData, 'audio/wav');
        const url = URL.createObjectURL(blob);
        setAudioUrl(url);
      } else {
        setError('No audio data received from server');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate speech');
    } finally {
      setIsGenerating(false);
    }
  };

  const base64ToBlob = (base64: string, contentType: string) => {
    const byteCharacters = atob(base64);
    const byteArrays = [];

    for (let offset = 0; offset < byteCharacters.length; offset += 512) {
      const slice = byteCharacters.slice(offset, offset + 512);
      const byteNumbers = new Array(slice.length);
      
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }
      
      const byteArray = new Uint8Array(byteNumbers);
      byteArrays.push(byteArray);
    }

    return new Blob(byteArrays, { type: contentType });
  };

  const downloadAudio = () => {
    if (!audioUrl) return;
    
    const a = document.createElement('a');
    a.href = audioUrl;
    a.download = `tts-${Date.now()}.wav`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const handleNewGeneration = () => {
    setText('');
    setAudioUrl(null);
    setError('');
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
    }
  };

  const voices = [
    { value: 'en-US-AvaMultilingualNeural', label: 'Ava (English, Female)' },
    { value: 'en-US-AndrewMultilingualNeural', label: 'Andrew (English, Male)' },
    { value: 'en-US-EmmaMultilingualNeural', label: 'Emma (English, Female)' },
    { value: 'en-US-BrianMultilingualNeural', label: 'Brian (English, Male)' },
  ];

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Text-to-Speech
          </h1>
          <p className="text-gray-600">
            Generate natural speech from text using Azure TTS
          </p>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        <div className="space-y-6">
          {/* Text Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Text to Convert
            </label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter the text you want to convert to speech..."
              rows={8}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
            <p className="mt-2 text-sm text-gray-500">
              {text.length} characters
            </p>
          </div>

          {/* Voice Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Voice
            </label>
            <select
              value={voice}
              onChange={(e) => setVoice(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              {voices.map((v) => (
                <option key={v.value} value={v.value}>
                  {v.label}
                </option>
              ))}
            </select>
          </div>

          {/* Generate Button */}
          <button
            onClick={handleGenerate}
            disabled={!text.trim() || isGenerating}
            className="w-full py-3 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            {isGenerating ? 'Generating...' : '🔊 Generate Speech'}
          </button>

          {/* Audio Player */}
          {audioUrl && (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 space-y-4">
              <h3 className="font-semibold text-gray-900">Generated Audio</h3>
              
              <audio
                ref={audioRef}
                controls
                src={audioUrl}
                className="w-full"
              />

              <div className="flex space-x-3">
                <button
                  onClick={downloadAudio}
                  className="flex-1 py-2 px-4 bg-green-600 text-white rounded-md hover:bg-green-700 font-medium"
                >
                  📥 Download Audio
                </button>
                <button
                  onClick={handleNewGeneration}
                  className="flex-1 py-2 px-4 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 font-medium"
                >
                  ✨ New Generation
                </button>
              </div>
            </div>
          )}

          {/* Info */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-semibold text-blue-900 mb-2">💡 Features</h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• High-quality HD voices powered by Azure</li>
              <li>• Fast generation (typically under 1 second)</li>
              <li>• Multiple voice options available</li>
              <li>• Download audio for offline use</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
