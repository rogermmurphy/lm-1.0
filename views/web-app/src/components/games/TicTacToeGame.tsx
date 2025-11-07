'use client'

import { useState, useEffect } from 'react'
import Monster from '@/components/Monster'

interface TicTacToeGameProps {
  onGameEnd: (won: boolean) => void
  onClose: () => void
}

type Player = 'X' | 'O' | null
type Board = Player[]

const INITIAL_BOARD: Board = Array(9).fill(null)

const WINNING_COMBINATIONS = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
  [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
  [0, 4, 8], [2, 4, 6] // Diagonals
]

export default function TicTacToeGame({ onGameEnd, onClose }: TicTacToeGameProps) {
  const [board, setBoard] = useState<Board>(INITIAL_BOARD)
  const [currentPlayer, setCurrentPlayer] = useState<Player>('X')
  const [winner, setWinner] = useState<Player | 'draw' | null>(null)
  const [winningLine, setWinningLine] = useState<number[] | null>(null)
  const [gameStarted, setGameStarted] = useState(false)

  const checkWinner = (board: Board): { winner: Player | 'draw' | null; line: number[] | null } => {
    // Check for winning combinations
    for (const combination of WINNING_COMBINATIONS) {
      const [a, b, c] = combination
      if (board[a] && board[a] === board[b] && board[a] === board[c]) {
        return { winner: board[a], line: combination }
      }
    }

    // Check for draw
    if (board.every(cell => cell !== null)) {
      return { winner: 'draw', line: null }
    }

    return { winner: null, line: null }
  }

  const makeMove = (index: number) => {
    if (board[index] || winner || !gameStarted) return

    const newBoard = [...board]
    newBoard[index] = currentPlayer
    setBoard(newBoard)

    const result = checkWinner(newBoard)
    if (result.winner) {
      setWinner(result.winner)
      setWinningLine(result.line)
    } else {
      setCurrentPlayer(currentPlayer === 'X' ? 'O' : 'X')
    }
  }

  const makeAIMove = () => {
    if (winner || currentPlayer === 'X') return

    // Simple AI: try to win, then block player, then random move
    const availableMoves = board.map((cell, index) => cell === null ? index : null).filter(val => val !== null) as number[]

    // Try to win
    for (const move of availableMoves) {
      const testBoard = [...board]
      testBoard[move] = 'O'
      if (checkWinner(testBoard).winner === 'O') {
        makeMove(move)
        return
      }
    }

    // Try to block player
    for (const move of availableMoves) {
      const testBoard = [...board]
      testBoard[move] = 'X'
      if (checkWinner(testBoard).winner === 'X') {
        makeMove(move)
        return
      }
    }

    // Take center if available
    if (availableMoves.includes(4)) {
      makeMove(4)
      return
    }

    // Take corners
    const corners = [0, 2, 6, 8]
    const availableCorners = corners.filter(corner => availableMoves.includes(corner))
    if (availableCorners.length > 0) {
      makeMove(availableCorners[Math.floor(Math.random() * availableCorners.length)])
      return
    }

    // Random move
    if (availableMoves.length > 0) {
      makeMove(availableMoves[Math.floor(Math.random() * availableMoves.length)])
    }
  }

  useEffect(() => {
    if (currentPlayer === 'O' && !winner && gameStarted) {
      const timer = setTimeout(makeAIMove, 500)
      return () => clearTimeout(timer)
    }
  }, [currentPlayer, winner, board, gameStarted])

  useEffect(() => {
    if (winner) {
      setTimeout(() => {
        if (winner === 'X') {
          onGameEnd(true) // Player wins
        } else {
          onGameEnd(false) // AI wins or draw
        }
      }, 1500)
    }
  }, [winner, onGameEnd])

  const resetGame = () => {
    setBoard(INITIAL_BOARD)
    setCurrentPlayer('X')
    setWinner(null)
    setWinningLine(null)
    setGameStarted(false)
  }

  const startGame = () => {
    setGameStarted(true)
  }

  const getCellContent = (index: number) => {
    const value = board[index]
    if (value === 'X') return '❌'
    if (value === 'O') return '⭕'
    return ''
  }

  const getCellStyle = (index: number) => {
    const isWinning = winningLine?.includes(index)
    return {
      width: '80px',
      height: '80px',
      border: '2px solid var(--border)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: '2rem',
      cursor: board[index] || winner || !gameStarted ? 'not-allowed' : 'pointer',
      backgroundColor: isWinning ? 'rgba(34, 197, 94, 0.2)' : 'var(--bg-secondary)',
      transition: 'all 0.2s ease',
      ':hover': {
        backgroundColor: !board[index] && !winner && gameStarted ? 'rgba(255, 255, 255, 0.1)' : undefined
      }
    }
  }

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
        minWidth: '400px'
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
          <h1 style={{ fontSize: '2rem', margin: 0, color: 'var(--text-primary)' }}>⭕ Tic-Tac-Toe</h1>
          <Monster size="md" baseColor="#EC4899" accentColor="#F472B6" animate={!winner} />
        </div>

        <div style={{ marginBottom: '20px' }}>
          {!gameStarted ? (
            <div>
              <div style={{ fontSize: '1.1rem', color: 'var(--text-primary)', marginBottom: '10px' }}>
                Ready to challenge the AI? 🤖
              </div>
              <div style={{ color: 'var(--muted)', fontSize: '0.9rem' }}>
                You are ❌ • AI is ⭕ • Get 3 in a row to win!
              </div>
            </div>
          ) : winner ? (
            <div>
              <div style={{ fontSize: '1.5rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '10px' }}>
                {winner === 'X' ? '🎉 You Win!' : winner === 'O' ? '🤖 AI Wins!' : '🤝 It\'s a Draw!'}
              </div>
              <div style={{ color: 'var(--muted)' }}>
                {winner === 'X' ? 'Great strategy!' : winner === 'O' ? 'Better luck next time!' : 'Good game!'}
              </div>
            </div>
          ) : (
            <div style={{ fontSize: '1.2rem', fontWeight: '600', color: 'var(--text-primary)' }}>
              {currentPlayer === 'X' ? '❌ Your Turn' : '⭕ AI Thinking...'}
            </div>
          )}
        </div>

        {!gameStarted ? (
          <button
            onClick={startGame}
            style={{
              background: '#EC4899',
              color: 'white',
              border: 'none',
              padding: '12px 24px',
              borderRadius: '8px',
              fontSize: '1.1rem',
              cursor: 'pointer',
              fontWeight: '600',
              marginBottom: '20px'
            }}
          >
            Start Game
          </button>
        ) : (
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(3, 1fr)', 
            gap: '4px', 
            margin: '20px auto',
            width: 'fit-content',
            padding: '10px',
            background: 'var(--bg-primary)',
            borderRadius: '12px'
          }}>
            {board.map((_, index) => (
              <div
                key={index}
                style={getCellStyle(index)}
                onClick={() => makeMove(index)}
              >
                {getCellContent(index)}
              </div>
            ))}
          </div>
        )}

        <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
          <button
            onClick={resetGame}
            style={{
              background: '#6B7280',
              color: 'white',
              border: 'none',
              padding: '8px 16px',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '0.9rem'
            }}
          >
            New Game
          </button>
        </div>

        <div style={{ marginTop: '20px', fontSize: '0.8rem', color: 'var(--muted)' }}>
          💡 Tip: Try to get three in a row while blocking the AI!
        </div>
      </div>
    </div>
  )
}
