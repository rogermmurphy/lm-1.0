'use client'

import { useState, useRef, useEffect } from 'react'
import Monster from '@/components/Monster'
import { chat } from '@/lib/api'

interface Message {
  id: number
  type: 'user' | 'ai'
  text: string
  timestamp?: Date
}

export default function GlobalAIChatbot() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    { 
      id: 1, 
      type: 'ai', 
      text: 'Hi! I\'m your Little Monster AI assistant! What can I help you study today?',
      timestamp: new Date()
    }
  ])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState<number | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Create conversation on first message
  const ensureConversation = async () => {
    if (!conversationId) {
      try {
        const response = await chat.createConversation('AI Assistant Chat')
        const newId = response.data?.id || response.data?.conversation_id
        if (newId) {
          setConversationId(newId)
          return newId
        }
      } catch (error) {
        console.error('Failed to create conversation:', error)
      }
    }
    return conversationId
  }

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now(),
      type: 'user',
      text: inputText,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputText('')
    setIsLoading(true)

    try {
      const currentConversationId = await ensureConversation()
      
      const response = await chat.sendMessage(inputText, currentConversationId || undefined)
      
      const aiMessage: Message = {
        id: Date.now() + 1,
        type: 'ai',
        text: response.data?.response || response.data?.message || 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, aiMessage])
      
    } catch (error: any) {
      console.error('Chat API error:', error)
      
      // Fallback response for when API is not available
      const fallbackResponse: Message = {
        id: Date.now() + 1,
        type: 'ai',
        text: 'I\'m having trouble connecting right now. Here are some things I can help with:\n\n• Math problems and explanations\n• Study tips and techniques\n• Assignment planning\n• Subject-specific questions\n\nTry asking me something specific!',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, fallbackResponse])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {/* Chat Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center text-white overflow-hidden"
        title="Chat with LM"
      >
        <Monster 
          size="sm" 
          baseColor="#FFFFFF" 
          accentColor="#E0E7FF" 
          animate={!isOpen}
          className="scale-75"
        />
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="absolute bottom-20 right-0 w-80 h-96 bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-4 text-white">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Monster size="sm" baseColor="#FFFFFF" accentColor="#E0E7FF" />
                <div>
                  <div className="font-semibold">Little Monster AI</div>
                  <div className="text-xs opacity-90">Always here to help!</div>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="text-white hover:bg-white/20 rounded-full p-1 transition-colors"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] p-3 rounded-2xl ${
                    message.type === 'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  <div className="text-sm whitespace-pre-wrap">{message.text}</div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-800 p-3 rounded-2xl">
                  <div className="flex items-center gap-2">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                    <span className="text-xs text-gray-500">LM is thinking...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Ask LM anything..."
                className="flex-1 px-3 py-2 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              <button
                onClick={handleSendMessage}
                className="px-4 py-2 bg-purple-500 text-white rounded-xl hover:bg-purple-600 transition-colors text-sm font-medium"
              >
                Send
              </button>
            </div>
            <div className="text-xs text-gray-500 mt-2">
              💡 Try: "Help me with math" or "Explain this concept"
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
