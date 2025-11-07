'use client'

import { useState, useRef, useEffect } from 'react'
import { chat } from '@/lib/api'
import { useTheme } from '@/contexts/ThemeContext'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export default function ChatBot() {
  const { themeColors } = useTheme()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState<number | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await chat.sendMessage(input, conversationId ?? undefined)
      
      if (!conversationId && response.data.conversation_id) {
        setConversationId(response.data.conversation_id)
      }
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.data.response || response.data.message || 'No response',
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (err: any) {
      console.error('Chat error:', err)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className={`p-4 ${themeColors.borderPrimary} border-b`}>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-2xl">🤖</span>
          <h3 className={`text-lg font-bold ${themeColors.textPrimary}`}>
            AI Assistant
          </h3>
        </div>
        <p className={`text-xs ${themeColors.textSecondary}`}>
          Always here to help
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-4xl mb-2">💬</div>
            <p className={`text-sm ${themeColors.textSecondary}`}>
              Ask me anything!
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${
                  message.role === 'user'
                    ? `${themeColors.accentPrimary} text-white`
                    : `${themeColors.cardBg} ${themeColors.cardBorder} border ${themeColors.textPrimary}`
                }`}
              >
                <div className="whitespace-pre-wrap break-words">
                  {message.content}
                </div>
                <div
                  className={`text-xs mt-1 ${
                    message.role === 'user' 
                      ? 'text-white opacity-70' 
                      : themeColors.textTertiary
                  }`}
                >
                  {message.timestamp.toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                  })}
                </div>
              </div>
            </div>
          ))
        )}

        {isLoading && (
          <div className="flex justify-start">
            <div className={`${themeColors.cardBg} ${themeColors.cardBorder} border rounded-lg px-3 py-2`}>
              <div className="flex space-x-1">
                <div className={`w-2 h-2 ${themeColors.accentPrimary} rounded-full animate-bounce`}></div>
                <div 
                  className={`w-2 h-2 ${themeColors.accentPrimary} rounded-full animate-bounce`}
                  style={{ animationDelay: '0.2s' }}
                ></div>
                <div 
                  className={`w-2 h-2 ${themeColors.accentPrimary} rounded-full animate-bounce`}
                  style={{ animationDelay: '0.4s' }}
                ></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className={`p-4 ${themeColors.borderPrimary} border-t`}>
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            className={`flex-1 px-3 py-2 text-sm ${themeColors.bgPrimary} ${themeColors.textPrimary} ${themeColors.borderPrimary} border rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-0 ${themeColors.accentPrimary.replace('bg-', 'focus:ring-')}`}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className={`px-4 py-2 text-sm font-medium text-white ${themeColors.accentPrimary} ${themeColors.accentHover} rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors`}
          >
            {isLoading ? '...' : '→'}
          </button>
        </div>
      </form>
    </div>
  )
}
