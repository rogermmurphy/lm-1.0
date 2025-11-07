'use client'

import { useState, useEffect, useCallback } from 'react'
import Monster from '@/components/Monster'

interface SnakeGameProps {
  onGameEnd: (won: boolean, score: number) => void
  onClose: () => void
}

interface Position {
  x: number
  y: number
}

const GRID_SIZE = 20
const GAME_SIZE = 400
const INITIAL_SNAKE = [{ x: 10, y: 10 }]
const INITIAL_FOOD = { x: 15, y: 15 }
const INITIAL_DIRECTION = { x: 0, y: -1 }

export default function SnakeGame({ onGameEnd, onClose }: SnakeGameProps) {
  const [snake, setSnake] = useState<Position[]>(INITIAL_SNAKE)
  const [food, setFood] = useState<Position>(INITIAL_FOOD)
  const [direction, setDirection] = useState<Position>(INITIAL_DIRECTION)
  const [gameStarted, setGameStarted] = useState(false)
  const [gameOver, setGameOver] = useState(false)
  const [score, setScore] = useState(0)
  const [isPaused, setIsPaused] = useState(false)

  const generateFood = useCallback((currentSnake: Position[]): Position => {
    let newFood: Position
    do {
      newFood = {
        x: Math.floor(Math.random() * GRID_SIZE),
        y: Math.floor(Math.random() * GRID_SIZE)
      }
    } while (currentSnake.some(segment => segment.x === newFood.x && segment.y === newFood.y))
    return newFood
  }, [])

  const resetGame = () => {
    setSnake(INITIAL_SNAKE)
    setFood(INITIAL_FOOD)
    setDirection(INITIAL_DIRECTION)
    setGameStarted(false)
    setGameOver(false)
    setScore(0)
    setIsPaused(false)
  }

  const moveSnake = useCallback(() => {
    if (!gameStarted || gameOver || isPaused) return

    setSnake(currentSnake => {
      const newSnake = [...currentSnake]
      const head = { 
        x: newSnake[0].x + direction.x, 
        y: newSnake[0].y + direction.y 
      }

      // Check wall collision
      if (head.x < 0 || head.x >= GRID_SIZE || head.y < 0 || head.y >= GRID_SIZE) {
        setGameOver(true)
        return currentSnake
      }

      // Check self collision
      if (newSnake.some(segment => segment.x === head.x && segment.y === head.y)) {
        setGameOver(true)
        return currentSnake
      }

      newSnake.unshift(head)

      // Check food collision
      if (head.x === food.x && head.y === food.y) {
        setScore(prev => prev + 10)
        setFood(generateFood(newSnake))
      } else {
        newSnake.pop()
      }

      return newSnake
    })
  }, [direction, food, gameStarted, gameOver, isPaused, generateFood])

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (!gameStarted && e.key === ' ') {
        setGameStarted(true)
        return
      }

      if (e.key === 'p' || e.key === 'P') {
        setIsPaused(prev => !prev)
        return
      }

      if (gameOver) return

      switch (e.key) {
        case 'ArrowUp':
          e.preventDefault()
          if (direction.y !== 1) setDirection({ x: 0, y: -1 })
          break
        case 'ArrowDown':
          e.preventDefault()
          if (direction.y !== -1) setDirection({ x: 0, y: 1 })
          break
        case 'ArrowLeft':
          e.preventDefault()
          if (direction.x !== 1) setDirection({ x: -1, y: 0 })
          break
        case 'ArrowRight':
          e.preventDefault()
          if (direction.x !== -1) setDirection({ x: 1, y: 0 })
          break
      }
    }

    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [direction, gameStarted, gameOver])

  useEffect(() => {
    const gameInterval = setInterval(moveSnake, 150)
    return () => clearInterval(gameInterval)
  }, [moveSnake])

  useEffect(() => {
    if (gameOver) {
      const won = score >= 50 // Win condition: score 50+ points
      setTimeout(() => onGameEnd(won, score), 1000)
    }
  }, [gameOver, score, onGameEnd])

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
        boxShadow: '0 20px 40px rgba(0,0,0,0.1)'
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
          <h1 style={{ fontSize: '2rem', margin: 0, color: 'var(--text-primary)' }}>🐍 Snake Game</h1>
          <Monster size="md" baseColor="#F59E0B" accentColor="#EAB308" animate={!gameOver} />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <div style={{ fontSize: '1.2rem', fontWeight: '600', color: 'var(--text-primary)' }}>
            Score: {score} | Length: {snake.length}
          </div>
          {!gameStarted && (
            <div style={{ color: 'var(--muted)', marginTop: '8px' }}>
              Press SPACE to start • Arrow keys to move • P to pause
            </div>
          )}
          {isPaused && gameStarted && (
            <div style={{ color: '#F59E0B', marginTop: '8px', fontWeight: '600' }}>
              PAUSED - Press P to continue
            </div>
          )}
        </div>

        <div
          style={{
            width: GAME_SIZE,
            height: GAME_SIZE,
            background: '#0f0e18',
            border: '3px solid var(--border)',
            borderRadius: '12px',
            position: 'relative',
            margin: '0 auto'
          }}
        >
          {/* Snake */}
          {snake.map((segment, index) => (
            <div
              key={index}
              style={{
                position: 'absolute',
                left: segment.x * (GAME_SIZE / GRID_SIZE),
                top: segment.y * (GAME_SIZE / GRID_SIZE),
                width: GAME_SIZE / GRID_SIZE - 1,
                height: GAME_SIZE / GRID_SIZE - 1,
                backgroundColor: index === 0 ? '#10B981' : '#34D399',
                borderRadius: '2px'
              }}
            />
          ))}

          {/* Food */}
          <div
            style={{
              position: 'absolute',
              left: food.x * (GAME_SIZE / GRID_SIZE),
              top: food.y * (GAME_SIZE / GRID_SIZE),
              width: GAME_SIZE / GRID_SIZE - 1,
              height: GAME_SIZE / GRID_SIZE - 1,
              backgroundColor: '#EF4444',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '12px'
            }}
          >
            🍎
          </div>

          {/* Game Over Overlay */}
          {gameOver && (
            <div
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                borderRadius: '12px',
                color: 'white'
              }}
            >
              <div style={{ fontSize: '2rem', marginBottom: '10px' }}>
                {score >= 50 ? '🏆 You Win!' : '💀 Game Over!'}
              </div>
              <div style={{ fontSize: '1.2rem', marginBottom: '20px' }}>
                Final Score: {score}
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
          )}

          {/* Start Screen */}
          {!gameStarted && !gameOver && (
            <div
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                borderRadius: '12px',
                color: 'white'
              }}
            >
              <div style={{ fontSize: '2rem', marginBottom: '20px' }}>🐍</div>
              <div style={{ fontSize: '1.2rem', marginBottom: '10px' }}>Press SPACE to Start</div>
              <div style={{ fontSize: '0.9rem', color: '#ccc' }}>
                Eat the red apples to grow! • Reach 50 points to win!
              </div>
            </div>
          )}
        </div>

        <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
          <button
            onClick={() => setIsPaused(!isPaused)}
            disabled={!gameStarted || gameOver}
            style={{
              background: isPaused ? '#10B981' : '#6B7280',
              color: 'white',
              border: 'none',
              padding: '8px 16px',
              borderRadius: '8px',
              cursor: gameStarted && !gameOver ? 'pointer' : 'not-allowed',
              opacity: gameStarted && !gameOver ? 1 : 0.5
            }}
          >
            {isPaused ? 'Resume' : 'Pause'}
          </button>
          <button
            onClick={resetGame}
            style={{
              background: '#EF4444',
              color: 'white',
              border: 'none',
              padding: '8px 16px',
              borderRadius: '8px',
              cursor: 'pointer'
            }}
          >
            Reset
          </button>
        </div>
      </div>
    </div>
  )
}
