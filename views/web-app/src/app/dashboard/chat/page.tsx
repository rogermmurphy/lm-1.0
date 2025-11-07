'use client';

import { useState, useRef, useEffect } from 'react';
import { chat } from '@/lib/api';
import ConversationList from '@/components/ConversationList';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(null);
  const [audioEnabled, setAudioEnabled] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [selectedVoice, setSelectedVoice] = useState('en-US-AriaNeural');
  const [availableVoices, setAvailableVoices] = useState<any[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load available voices and user preference
  useEffect(() => {
    // Load saved voice preference from localStorage
    const savedVoice = localStorage.getItem('preferredVoice');
    if (savedVoice) {
      setSelectedVoice(savedVoice);
    }

    // Fetch available voices from API
    console.log('[Chat] Fetching voices from /api/chat/voices');
    chat.getVoices()
      .then((response) => {
        console.log('[Chat] Voices response:', response.data);
        setAvailableVoices(response.data.voices || []);
        console.log('[Chat] Available voices set:', response.data.voices?.length || 0);
      })
      .catch((error) => {
        console.error('[Chat] Failed to load voices:', error);
        console.error('[Chat] Error details:', error.response?.data, error.message);
      });
  }, []);

  // Save voice preference to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('preferredVoice', selectedVoice);
  }, [selectedVoice]);

  // Helper function to convert base64 to blob
  const base64ToBlob = (base64: string, mimeType: string): Blob => {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
  };

  // TTS: Play audio for AI response
  const playAudio = async (text: string) => {
    try {
      const result = await chat.speak(text, selectedVoice);
      if (result.data.success && result.data.audio_base64) {
        const audioBlob = base64ToBlob(result.data.audio_base64, 'audio/wav');
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
        // Clean up URL after playing
        audio.onended = () => URL.revokeObjectURL(audioUrl);
      }
    } catch (error) {
      console.error('TTS error:', error);
    }
  };

  // STT: Start recording
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

  // STT: Stop recording
  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError('');

    try {
      // Send message with current conversation ID (creates new if null)
      const response = await chat.sendMessage(input, currentConversationId ?? undefined);
      
      // Update conversation ID if this was a new conversation
      if (!currentConversationId && response.data.conversation_id) {
        setCurrentConversationId(response.data.conversation_id);
      }
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.data.response || response.data.message || 'No response',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // Auto-play audio if enabled
      if (audioEnabled && assistantMessage.content) {
        playAudio(assistantMessage.content);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get response from AI');
      console.error('Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewConversation = () => {
    setMessages([]);
    setError('');
    setCurrentConversationId(null);
  };

  const handleSelectConversation = async (conversationId: number) => {
    // Load conversation history from API
    console.log('[Chat] Loading conversation:', conversationId);
    setError('');
    setCurrentConversationId(conversationId);
    setIsLoading(true);
    
    try {
      const response = await chat.getConversationMessages(conversationId);
      console.log('[Chat] API response:', response);
      console.log('[Chat] Messages data:', response.data);
      
      // Handle both possible response formats
      const messagesArray = response.data.messages || response.data || [];
      console.log('[Chat] Messages array:', messagesArray);
      
      const loadedMessages = messagesArray.map((msg: any) => ({
        id: msg.id.toString(),
        role: msg.role,
        content: msg.content,
        timestamp: new Date(msg.timestamp)
      }));
      
      console.log('[Chat] Loaded messages:', loadedMessages);
      setMessages(loadedMessages);
      console.log('[Chat] Messages set, length:', loadedMessages.length);
    } catch (err: any) {
      setError('Failed to load conversation history');
      console.error('[Chat] Load conversation error:', err);
      setMessages([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-[calc(100vh-4rem)] flex">
      {/* Conversation List Sidebar */}
      <ConversationList
        selectedConversationId={currentConversationId}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-white">
        {/* Header */}
        <div className="px-6 py-4 border-b-2 border-lmPink/30 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-lmGray">AI Tutor Chat</h1>
            <p className="text-sm text-lmGray/70">
              {currentConversationId 
                ? `Conversation #${currentConversationId}` 
                : 'Start a new conversation'}
            </p>
          </div>
          {currentConversationId && (
            <button
              onClick={handleNewConversation}
              className="px-4 py-2 text-sm font-medium text-lmGray bg-lmCream hover:bg-lmPink/10 border border-lmPink/30 rounded-md"
            >
              ✨ New Chat
            </button>
          )}
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">💬</div>
              <h3 className="text-lg font-semibold text-lmGray mb-2">
                Start a Conversation
              </h3>
              <p className="text-lmGray/70 mb-4">
                Ask me anything! I'm here to help with your studies.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
                <button
                  onClick={() => setInput('Explain quantum physics in simple terms')}
                  className="p-3 text-left bg-lmCream hover:bg-lmPink/10 border border-lmPink/30 rounded-lg text-sm transition-colors"
                >
                  <span className="font-medium text-lmGray">Explain quantum physics</span>
                  <br />
                  <span className="text-lmGray/70">in simple terms</span>
                </button>
                <button
                  onClick={() => setInput('Help me understand calculus derivatives')}
                  className="p-3 text-left bg-lmCream hover:bg-lmPink/10 border border-lmPink/30 rounded-lg text-sm transition-colors"
                >
                  <span className="font-medium text-lmGray">Help with calculus</span>
                  <br />
                  <span className="text-lmGray/70">derivatives explained</span>
                </button>
                <button
                  onClick={() => setInput('What are the main causes of World War II?')}
                  className="p-3 text-left bg-lmCream hover:bg-lmPink/10 border border-lmPink/30 rounded-lg text-sm transition-colors"
                >
                  <span className="font-medium text-lmGray">World War II causes</span>
                  <br />
                  <span className="text-lmGray/70">historical context</span>
                </button>
                <button
                  onClick={() => setInput('Explain photosynthesis step by step')}
                  className="p-3 text-left bg-lmCream hover:bg-lmPink/10 border border-lmPink/30 rounded-lg text-sm transition-colors"
                >
                  <span className="font-medium text-lmGray">Photosynthesis process</span>
                  <br />
                  <span className="text-lmGray/70">step-by-step guide</span>
                </button>
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg px-4 py-3 ${
                    message.role === 'user'
                      ? 'bg-lmPink text-white'
                      : 'bg-lmCream border border-lmPink/30 text-lmGray'
                  }`}
                >
                  <div className="whitespace-pre-wrap break-words">{message.content}</div>
                  <div
                    className={`text-xs mt-2 ${
                      message.role === 'user' ? 'text-white/70' : 'text-lmGray/60'
                    }`}
                  >
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))
          )}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-lmCream border border-lmPink/30 rounded-lg px-4 py-3">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-lmPurple rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-lmPurple rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-lmPurple rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form onSubmit={handleSubmit} className="px-6 py-4 border-t-2 border-lmPink/30">
          <div className="flex space-x-3">
            <button
              type="button"
              onClick={() => setAudioEnabled(!audioEnabled)}
              className="px-3 py-3 bg-lmCream hover:bg-lmPink/10 border border-lmPink/30 rounded-lg"
              title={audioEnabled ? 'Disable Audio' : 'Enable Audio'}
            >
              {audioEnabled ? '🔊' : '🔇'}
            </button>
            {audioEnabled && availableVoices.length > 0 && (
              <select
                value={selectedVoice}
                onChange={(e) => setSelectedVoice(e.target.value)}
                className="px-3 py-2 bg-lmCream hover:bg-lmPink/10 border border-lmPink/30 rounded-lg text-sm text-lmGray focus:outline-none focus:ring-2 focus:ring-lmPurple"
                title="Select Voice"
              >
                {availableVoices.map((voice) => (
                  <option key={voice.id} value={voice.id}>
                    {voice.name}
                  </option>
                ))}
              </select>
            )}
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
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your question here..."
              className="flex-1 px-4 py-3 border border-lmPink/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-lmPurple"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="px-6 py-3 bg-lmPink text-white rounded-lg hover:bg-lmPink/90 focus:outline-none focus:ring-2 focus:ring-lmPurple disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </div>
          <div className="flex justify-between items-center mt-2">
            <p className="text-xs text-lmGray/60">
              💡 Powered by AWS Bedrock Claude 3 Sonnet with RAG-enhanced responses
            </p>
            <div className="flex items-center space-x-4 text-xs text-lmGray/60">
              {audioEnabled && <span>🔊 Audio enabled</span>}
              {isRecording && <span className="text-red-500">🔴 Recording...</span>}
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
