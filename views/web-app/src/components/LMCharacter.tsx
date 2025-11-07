'use client'

import { useState, useEffect } from 'react'
import Monster from '@/components/Monster'

export default function LMCharacter() {
  const [showSpeech, setShowSpeech] = useState(false)
  const [currentMessage, setCurrentMessage] = useState('')

  const messages = [
    "Ready to study together? 📚",
    "You're doing great! Keep going! ✨",
    "Let's make learning fun today! 🎮", 
    "I believe in you! 💪",
    "Take breaks when you need them! 😊",
    "Every small step counts! 🌟",
    "Learning is an adventure! 🚀"
  ]

  useEffect(() => {
    // Show initial message after 2 seconds
    const timer = setTimeout(() => {
      setCurrentMessage(messages[0])
      setShowSpeech(true)
      
      // Hide after 4 seconds
      setTimeout(() => {
        setShowSpeech(false)
      }, 4000)
    }, 2000)

    return () => clearTimeout(timer)
  }, [])

  const handleClick = () => {
    const randomMessage = messages[Math.floor(Math.random() * messages.length)]
    setCurrentMessage(randomMessage)
    setShowSpeech(true)

    // Hide after 3 seconds
    setTimeout(() => {
      setShowSpeech(false)
    }, 3000)
  }

  return (
    <div className="lm-character">
      {showSpeech && (
        <div className={`lm-speech ${showSpeech ? 'show' : ''}`}>
          {currentMessage}
        </div>
      )}
      <div className="lm-avatar" onClick={handleClick}>
        <Monster 
          size="sm" 
          baseColor="#FFFFFF" 
          accentColor="#E0E7FF"
          animate={true}
          className="scale-75"
        />
      </div>
    </div>
  )
}
