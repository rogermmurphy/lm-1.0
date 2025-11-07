'use client'

import { useState, useEffect } from 'react'
import Monster from '@/components/Monster'

interface QuizArenaProps {
  onGameEnd: (won: boolean, score: number) => void
  onClose: () => void
}

interface Question {
  id: number
  question: string
  options: string[]
  correct: number
  category: string
  difficulty: 'easy' | 'medium' | 'hard'
}

const SAMPLE_QUESTIONS: Question[] = [
  {
    id: 1,
    question: "What is 2 + 2?",
    options: ["3", "4", "5", "6"],
    correct: 1,
    category: "Math",
    difficulty: "easy"
  },
  {
    id: 2,
    question: "Which planet is closest to the Sun?",
    options: ["Venus", "Earth", "Mercury", "Mars"],
    correct: 2,
    category: "Science",
    difficulty: "easy"
  },
  {
    id: 3,
    question: "What is the capital of France?",
    options: ["London", "Berlin", "Paris", "Madrid"],
    correct: 2,
    category: "Geography",
    difficulty: "easy"
  },
  {
    id: 4,
    question: "What is 15 × 7?",
    options: ["95", "105", "115", "125"],
    correct: 1,
    category: "Math",
    difficulty: "medium"
  },
  {
    id: 5,
    question: "Who wrote 'Romeo and Juliet'?",
    options: ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
    correct: 1,
    category: "Literature",
    difficulty: "medium"
  },
  {
    id: 6,
    question: "What is the chemical symbol for gold?",
    options: ["Go", "Gd", "Au", "Ag"],
    correct: 2,
    category: "Science",
    difficulty: "medium"
  },
  {
    id: 7,
    question: "In which year did World War II end?",
    options: ["1944", "1945", "1946", "1947"],
    correct: 1,
    category: "History",
    difficulty: "medium"
  },
  {
    id: 8,
    question: "What is the square root of 144?",
    options: ["11", "12", "13", "14"],
    correct: 1,
    category: "Math",
    difficulty: "medium"
  }
]

export default function QuizArena({ onGameEnd, onClose }: QuizArenaProps) {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [questions, setQuestions] = useState<Question[]>([])
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [score, setScore] = useState(0)
  const [correctAnswers, setCorrectAnswers] = useState(0)
  const [gameStarted, setGameStarted] = useState(false)
  const [gameEnded, setGameEnded] = useState(false)
  const [showResult, setShowResult] = useState(false)
  const [timeLeft, setTimeLeft] = useState(15)
  const [answeredQuestions, setAnsweredQuestions] = useState<boolean[]>([])

  useEffect(() => {
    // Shuffle questions and take 8 for the quiz
    const shuffled = [...SAMPLE_QUESTIONS].sort(() => Math.random() - 0.5).slice(0, 8)
    setQuestions(shuffled)
    setAnsweredQuestions(new Array(8).fill(false))
  }, [])

  useEffect(() => {
    let timer: NodeJS.Timeout
    if (gameStarted && !gameEnded && !showResult && timeLeft > 0) {
      timer = setTimeout(() => {
        setTimeLeft(prev => prev - 1)
      }, 1000)
    } else if (timeLeft === 0 && !showResult) {
      // Time's up, auto-submit as wrong answer
      handleAnswer(-1) // -1 indicates timeout
    }

    return () => clearTimeout(timer)
  }, [timeLeft, gameStarted, gameEnded, showResult])

  const startGame = () => {
    setGameStarted(true)
    setTimeLeft(15)
  }

  const handleAnswer = (answerIndex: number) => {
    if (showResult || gameEnded) return

    setSelectedAnswer(answerIndex)
    setShowResult(true)

    const isCorrect = answerIndex === questions[currentQuestion].correct
    if (isCorrect) {
      const points = getPointsForDifficulty(questions[currentQuestion].difficulty)
      setScore(prev => prev + points)
      setCorrectAnswers(prev => prev + 1)
    }

    const newAnsweredQuestions = [...answeredQuestions]
    newAnsweredQuestions[currentQuestion] = true
    setAnsweredQuestions(newAnsweredQuestions)

    // Auto-advance after showing result
    setTimeout(() => {
      if (currentQuestion + 1 < questions.length) {
        nextQuestion()
      } else {
        endGame()
      }
    }, 2000)
  }

  const nextQuestion = () => {
    setCurrentQuestion(prev => prev + 1)
    setSelectedAnswer(null)
    setShowResult(false)
    setTimeLeft(15)
  }

  const endGame = () => {
    setGameEnded(true)
    setTimeout(() => {
      const won = correctAnswers >= 5 // Win if 5+ correct answers
      onGameEnd(won, score)
    }, 2000)
  }

  const getPointsForDifficulty = (difficulty: string): number => {
    switch (difficulty) {
      case 'easy': return 10
      case 'medium': return 20
      case 'hard': return 30
      default: return 10
    }
  }

  const resetGame = () => {
    setCurrentQuestion(0)
    setSelectedAnswer(null)
    setScore(0)
    setCorrectAnswers(0)
    setGameStarted(false)
    setGameEnded(false)
    setShowResult(false)
    setTimeLeft(15)
    setAnsweredQuestions(new Array(8).fill(false))
    
    // Shuffle questions again
    const shuffled = [...SAMPLE_QUESTIONS].sort(() => Math.random() - 0.5).slice(0, 8)
    setQuestions(shuffled)
  }

  if (questions.length === 0) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        background: 'var(--bg-primary)', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center'
      }}>
        <div>Loading questions...</div>
      </div>
    )
  }

  const question = questions[currentQuestion]

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'var(--bg-primary)', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div style={{ 
        background: 'var(--bg-secondary)', 
        borderRadius: '20px', 
        padding: '30px', 
        textAlign: 'center',
        boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
        minWidth: '500px',
        maxWidth: '700px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px', marginBottom: '20px' }}>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '1.5rem',
              color: 'var(--text-primary)',
              cursor: 'pointer',
              padding: '8px'
            }}
          >
            ← Back
          </button>
          <h1 style={{ fontSize: '2rem', margin: 0, color: 'var(--text-primary)' }}>⚔️ Quiz Arena</h1>
          <Monster size="md" baseColor="#EF4444" accentColor="#F87171" animate={!gameEnded} />
        </div>

        {!gameStarted ? (
          <div>
            <div style={{ marginBottom: '20px' }}>
              <div style={{ fontSize: '1.2rem', color: 'var(--text-primary)', marginBottom: '10px' }}>
                Ready for the Challenge? 🎯
              </div>
              <div style={{ color: 'var(--muted)', fontSize: '0.9rem', lineHeight: '1.5' }}>
                • 8 Questions from various subjects<br/>
                • 15 seconds per question<br/>
                • Get 5+ correct to win!<br/>
                • Different difficulties = Different points
              </div>
            </div>
            <button
              onClick={startGame}
              style={{
                background: '#EF4444',
                color: 'white',
                border: 'none',
                padding: '12px 24px',
                borderRadius: '8px',
                fontSize: '1.1rem',
                cursor: 'pointer',
                fontWeight: '600'
              }}
            >
              Start Quiz Arena
            </button>
          </div>
        ) : gameEnded ? (
          <div>
            <div style={{ fontSize: '1.5rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '20px' }}>
              {correctAnswers >= 5 ? '🏆 Victory!' : '💪 Good Effort!'}
            </div>
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', 
              gap: '20px',
              marginBottom: '20px',
              textAlign: 'center'
            }}>
              <div>
                <div style={{ fontSize: '2rem', fontWeight: '700', color: '#EF4444' }}>{score}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--muted)' }}>Total Score</div>
              </div>
              <div>
                <div style={{ fontSize: '2rem', fontWeight: '700', color: '#10B981' }}>{correctAnswers}/8</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--muted)' }}>Correct</div>
              </div>
              <div>
                <div style={{ fontSize: '2rem', fontWeight: '700', color: '#F59E0B' }}>
                  {Math.round((correctAnswers / 8) * 100)}%
                </div>
                <div style={{ fontSize: '0.8rem', color: 'var(--muted)' }}>Accuracy</div>
              </div>
            </div>
            <button
              onClick={resetGame}
              style={{
                background: '#10B981',
                color: 'white',
                border: 'none',
                padding: '12px 24px',
                borderRadius: '8px',
                fontSize: '1rem',
                cursor: 'pointer',
                fontWeight: '600'
              }}
            >
              Play Again
            </button>
          </div>
        ) : (
          <div>
            {/* Progress Bar */}
            <div style={{ marginBottom: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <span style={{ color: 'var(--text-primary)', fontWeight: '600' }}>
                  Question {currentQuestion + 1} of {questions.length}
                </span>
                <span style={{ color: 'var(--text-primary)', fontWeight: '600' }}>
                  Score: {score}
                </span>
              </div>
              <div style={{ 
                width: '100%', 
                height: '8px', 
                background: 'var(--bg-primary)', 
                borderRadius: '4px',
                overflow: 'hidden'
              }}>
                <div style={{ 
                  width: `${((currentQuestion + 1) / questions.length) * 100}%`, 
                  height: '100%', 
                  background: '#EF4444',
                  transition: 'width 0.3s ease'
                }}></div>
              </div>
            </div>

            {/* Timer */}
            <div style={{ 
              marginBottom: '20px',
              fontSize: '1.2rem',
              fontWeight: '600',
              color: timeLeft <= 5 ? '#EF4444' : 'var(--text-primary)'
            }}>
              ⏰ {timeLeft}s
            </div>

            {/* Question */}
            <div style={{ marginBottom: '30px' }}>
              <div style={{ 
                display: 'inline-block',
                background: 'rgba(239, 68, 68, 0.1)',
                color: '#EF4444',
                padding: '4px 12px',
                borderRadius: '12px',
                fontSize: '0.8rem',
                fontWeight: '600',
                marginBottom: '15px'
              }}>
                {question.category} • {question.difficulty}
              </div>
              <h2 style={{ 
                fontSize: '1.3rem', 
                lineHeight: '1.4',
                color: 'var(--text-primary)',
                margin: 0
              }}>
                {question.question}
              </h2>
            </div>

            {/* Options */}
            <div style={{ display: 'grid', gap: '12px', marginBottom: '20px' }}>
              {question.options.map((option, index) => {
                let backgroundColor = 'var(--bg-secondary)'
                let borderColor = 'var(--border)'
                let textColor = 'var(--text-primary)'

                if (showResult) {
                  if (index === question.correct) {
                    backgroundColor = 'rgba(34, 197, 94, 0.2)'
                    borderColor = '#22C55E'
                    textColor = '#22C55E'
                  } else if (index === selectedAnswer) {
                    backgroundColor = 'rgba(239, 68, 68, 0.2)'
                    borderColor = '#EF4444'
                    textColor = '#EF4444'
                  }
                }

                return (
                  <button
                    key={index}
                    onClick={() => handleAnswer(index)}
                    disabled={showResult}
                    style={{
                      padding: '15px',
                      border: `2px solid ${borderColor}`,
                      borderRadius: '12px',
                      background: backgroundColor,
                      color: textColor,
                      fontSize: '1rem',
                      cursor: showResult ? 'default' : 'pointer',
                      transition: 'all 0.2s ease',
                      textAlign: 'left'
                    }}
                  >
                    <span style={{ fontWeight: '600', marginRight: '8px' }}>
                      {String.fromCharCode(65 + index)}.
                    </span>
                    {option}
                  </button>
                )
              })}
            </div>

            {/* Answer feedback */}
            {showResult && (
              <div style={{ 
                padding: '15px',
                borderRadius: '12px',
                backgroundColor: selectedAnswer === question.correct ? 'rgba(34, 197, 94, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                color: selectedAnswer === question.correct ? '#22C55E' : '#EF4444',
                fontWeight: '600'
              }}>
                {selectedAnswer === question.correct ? (
                  '✅ Correct! +' + getPointsForDifficulty(question.difficulty) + ' points'
                ) : selectedAnswer === -1 ? (
                  '⏰ Time\'s up!'
                ) : (
                  '❌ Wrong answer'
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
