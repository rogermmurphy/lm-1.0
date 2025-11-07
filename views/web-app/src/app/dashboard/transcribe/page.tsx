'use client';

import { useState } from 'react';
import { transcription } from '@/lib/api';

interface TranscriptionJob {
  jobId: number;
  filename: string;
  status: string;
  transcript?: string;
  created_at: string;
}

export default function TranscribePage() {
  const [file, setFile] = useState<File | null>(null);
  const [language, setLanguage] = useState('en');
  const [isUploading, setIsUploading] = useState(false);
  const [currentJob, setCurrentJob] = useState<TranscriptionJob | null>(null);
  const [error, setError] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      
      // Validate file type
      const validTypes = ['audio/mpeg', 'audio/wav', 'audio/x-m4a', 'audio/mp4'];
      if (!validTypes.includes(selectedFile.type)) {
        setError('Please upload an audio file (MP3, WAV, or M4A)');
        return;
      }
      
      // Validate file size (max 50MB)
      if (selectedFile.size > 50 * 1024 * 1024) {
        setError('File size must be less than 50MB');
        return;
      }
      
      setFile(selectedFile);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setError('');

    try {
      const response = await transcription.upload(file, language);
      const job: TranscriptionJob = {
        jobId: response.data.job_id,
        filename: file.name,
        status: 'processing',
        created_at: new Date().toISOString(),
      };
      
      setCurrentJob(job);
      
      // Poll for job status
      pollJobStatus(job.jobId);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload file');
    } finally {
      setIsUploading(false);
    }
  };

  const pollJobStatus = async (jobId: number) => {
    const maxAttempts = 60; // 5 minutes max
    let attempts = 0;

    const poll = setInterval(async () => {
      attempts++;
      
      try {
        const statusResponse = await transcription.getJobStatus(jobId);
        const status = statusResponse.data.status;

        setCurrentJob((prev) => prev ? { ...prev, status } : null);

        if (status === 'completed') {
          clearInterval(poll);
          
          // Get transcript
          const resultResponse = await transcription.getResult(jobId);
          setCurrentJob((prev) => prev ? {
            ...prev,
            status: 'completed',
            transcript: resultResponse.data.transcript
          } : null);
        } else if (status === 'failed') {
          clearInterval(poll);
          setError('Transcription failed. Please try again.');
        } else if (attempts >= maxAttempts) {
          clearInterval(poll);
          setError('Transcription timed out. Please try again.');
        }
      } catch (err) {
        clearInterval(poll);
        setError('Failed to check job status');
      }
    }, 5000); // Check every 5 seconds
  };

  const handleNewTranscription = () => {
    setFile(null);
    setCurrentJob(null);
    setError('');
  };

  const downloadTranscript = () => {
    if (!currentJob?.transcript) return;
    
    const blob = new Blob([currentJob.transcript], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `transcript-${currentJob.filename}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6 border-2 border-lmPink/30">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-lmGray mb-2">
            Audio Transcription
          </h1>
          <p className="text-lmGray/70">
            Convert audio recordings to text using Whisper AI
          </p>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {!currentJob ? (
          <div className="space-y-6">
            {/* File Upload */}
            <div>
              <label className="block text-sm font-medium text-lmGray mb-2">
                Select Audio File
              </label>
              <div className="flex items-center space-x-4">
                <input
                  type="file"
                  accept="audio/mpeg,audio/wav,audio/x-m4a,audio/mp4"
                  onChange={handleFileChange}
                  className="block w-full text-sm text-lmGray
                    file:mr-4 file:py-2 file:px-4
                    file:rounded-md file:border-0
                    file:text-sm file:font-semibold
                    file:bg-lmPink/20 file:text-lmGray
                    hover:file:bg-lmPink/30"
                />
              </div>
              {file && (
                <p className="mt-2 text-sm text-lmGray/70">
                  Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                </p>
              )}
            </div>

            {/* Language Selection */}
            <div>
              <label className="block text-sm font-medium text-lmGray mb-2">
                Language
              </label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="block w-full px-3 py-2 border border-lmPink/30 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-lmPurple"
              >
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
                <option value="zh">Chinese</option>
              </select>
            </div>

            {/* Upload Button */}
            <button
              onClick={handleUpload}
              disabled={!file || isUploading}
              className="w-full py-3 px-4 bg-lmPink text-white rounded-md hover:bg-lmPink/90 focus:outline-none focus:ring-2 focus:ring-lmPurple disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {isUploading ? 'Uploading...' : 'Upload and Transcribe'}
            </button>

            {/* Info */}
            <div className="bg-gradient-to-r from-lmCream to-lmPink/20 border-2 border-lmPink/30 rounded-lg p-4">
              <h3 className="font-semibold text-lmGray mb-2">📋 Supported Formats</h3>
              <ul className="text-sm text-lmGray/80 space-y-1">
                <li>• MP3, WAV, M4A audio files</li>
                <li>• Maximum file size: 50MB</li>
                <li>• Typical transcription time: ~30 seconds for 5 minutes of audio</li>
              </ul>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Job Status */}
            <div className="bg-lmCream border-2 border-lmPink/30 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold text-lmGray">Transcription Status</h3>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  currentJob.status === 'completed' ? 'bg-green-100 text-green-800' :
                  currentJob.status === 'processing' ? 'bg-lmPurple/20 text-lmPurple' :
                  'bg-red-100 text-red-800'
                }`}>
                  {currentJob.status}
                </span>
              </div>
              <p className="text-sm text-lmGray/70">
                File: {currentJob.filename}
              </p>
              {currentJob.status === 'processing' && (
                <div className="mt-4">
                  <div className="w-full bg-lmCream border border-lmPink/30 rounded-full h-2">
                    <div className="bg-lmPurple h-2 rounded-full animate-pulse" style={{ width: '70%' }}></div>
                  </div>
                  <p className="text-xs text-lmGray/60 mt-2">Processing... This may take a minute.</p>
                </div>
              )}
            </div>

            {/* Transcript Display */}
            {currentJob.transcript && (
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="font-semibold text-lmGray">Transcript</h3>
                  <button
                    onClick={downloadTranscript}
                    className="px-4 py-2 text-sm font-medium text-lmPurple bg-lmPurple/10 hover:bg-lmPurple/20 border border-lmPurple/30 rounded-md"
                  >
                    📥 Download
                  </button>
                </div>
                <div className="bg-white border-2 border-lmPink/30 rounded-lg p-4 max-h-96 overflow-y-auto">
                  <p className="text-lmGray whitespace-pre-wrap">{currentJob.transcript}</p>
                </div>
              </div>
            )}

            {/* New Transcription Button */}
            <button
              onClick={handleNewTranscription}
              className="w-full py-3 px-4 bg-lmCream border border-lmPink/30 text-lmGray rounded-md hover:bg-lmPink/10 focus:outline-none font-medium"
            >
              ✨ New Transcription
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
