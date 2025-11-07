'use client'

import { useState } from 'react'
import Monster from '@/components/Monster'
import { useGameState } from '@/hooks/useGameState'

// Import game components
import SnakeGame from '@/components/games/SnakeGame'
import TicTacToeGame from '@/components/games/TicTacToeGame'
import QuizArena from '@/components/games/QuizArena'

export default function GamesPage() {
  const { stats, leaderboard, recordGameWin, recordGameLoss, addXP } = useGameState()
  const [activeGame, setActiveGame] = useState<string | null>(null)

  const games = [
    {
      name: 'Learn Mode',
      desc: 'Adaptive mode with hints and flash cards.',
      icon: '🧠',
      color: '#10B981',
      implemented: false
    },
    {
      name: 'Flash Cards', 
      desc: 'Practice your topics with quick flash cards.',
      icon: '🃏',
      color: '#3B82F6',
      implemented: false
    },
    {
      name: 'Monster Dash',
      desc: 'Run & collect points while sharpening focus.',
      icon: '👾',
      color: '#8B5CF6',
      implemented: false
    },
    {
      name: 'Quiz Arena',
      desc: 'Battle with timed quizzes.',
      icon: '⚔️',
      color: '#EF4444',
      implemented: true
    },
    {
      name: 'Snake',
      desc: 'Classic game to relax your mind.',
      icon: '🐍',
      color: '#F59E0B',
      implemented: true
    },
    {
      name: '2048',
      desc: 'Combine numbers to reach 2048.',
      icon: '🔢',
      color: '#06B6D4',
      implemented: false
    },
    {
      name: 'Tic-Tac-Toe',
      desc: 'Quick strategy game for mental breaks.',
      icon: '⭕',
      color: '#EC4899',
      implemented: true
    },
    {
      name: 'Milkshake Maker',
      desc: 'Create fun milkshakes and unwind.',
      icon: '🥤',
      color: '#84CC16',
      implemented: false
    }
  ]

  const handleGameClick = (gameName: string, implemented: boolean) => {
    if (!implemented) {
      alert(`${gameName} is coming soon! Try Snake, Tic-Tac-Toe, or Quiz Arena for now.`)
      return
    }
    
    setActiveGame(gameName)
  }

  const handleGameEnd = (won: boolean, gameType: string, score?: number) => {
    if (won) {
      recordGameWin(gameType)
      if (score) {
        addXP(Math.floor(score / 10)) // Bonus XP based on score
      }
    } else {
      recordGameLoss(gameType)
    }
    setActiveGame(null)
  }

  // If a game is active, show the game component
  if (activeGame === 'Snake') {
    return <SnakeGame onGameEnd={(won, score) => handleGameEnd(won, 'Snake', score)} onClose={() => setActiveGame(null)} />
  }
  
  if (activeGame === 'Tic-Tac-Toe') {
    return <TicTacToeGame onGameEnd={(won) => handleGameEnd(won, 'Tic-Tac-Toe')} onClose={() => setActiveGame(null)} />
  }
  
  if (activeGame === 'Quiz Arena') {
    return <QuizArena onGameEnd={(won, score) => handleGameEnd(won, 'Quiz Arena', score)} onClose={() => setActiveGame(null)} />
  }

  return (
    <div className="games-layout">
      <div style={{ marginBottom: '30px' }}>
        <h1 style={{ 
          fontSize: '2rem', 
          fontWeight: '700', 
          marginBottom: '8px',
          color: '#ffffff'
        }}>
          Games 🎮
        </h1>
        <p style={{ color: 'var(--muted)', fontSize: '1.1rem' }}>
          Play games that make learning fun while earning XP and LM Coins
        </p>
      </div>

      {/* Progress Stats */}
      <div className="widget-card" style={{ marginBottom: '40px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <h4>Your Gaming Progress</h4>
          <Monster size="md" baseColor="var(--lm-pink)" accentColor="var(--lm-purple)" glow="soft" animate={true} />
        </div>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', 
          gap: '20px',
          textAlign: 'center'
        }}>
          <div>
            <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--lm-purple)' }}>{stats.xp.toLocaleString()}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--muted)' }}>XP Points</div>
          </div>
          <div>
            <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--lm-pink)' }}>🪙 {stats.coins}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--muted)' }}>LM Coins</div>
          </div>
          <div>
            <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#fbbf24' }}>Level {stats.level}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--muted)' }}>Monster Level</div>
          </div>
          <div>
            <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#34d399' }}>{stats.gamesWon}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--muted)' }}>Games Won</div>
          </div>
        </div>
      </div>

      {/* Games Grid */}
      <div className="games-grid">
        {games.map((game) => (
          <div 
            key={game.name} 
            className={`game-card ${!game.implemented ? 'opacity-60' : ''}`}
            onClick={() => handleGameClick(game.name, game.implemented)}
            style={{ 
              cursor: game.implemented ? 'pointer' : 'not-allowed',
              position: 'relative'
            }}
          >
            {!game.implemented && (
              <div style={{ 
                position: 'absolute',
                top: '8px',
                right: '8px',
                background: 'rgba(255, 193, 7, 0.9)',
                color: '#000',
                fontSize: '0.7rem',
                padding: '2px 6px',
                borderRadius: '8px',
                fontWeight: '600'
              }}>
                Coming Soon
              </div>
            )}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '16px' }}>
              <div className="game-icon">{game.icon}</div>
              <Monster 
                size="sm" 
                baseColor={game.color} 
                accentColor={game.color}
                glow="soft"
                className="opacity-75"
              />
            </div>
            <h2>{game.name}</h2>
            <p>{game.desc}</p>
          </div>
        ))}
      </div>

      {/* Leaderboard */}
      <div className="widget-card" style={{ marginTop: '50px' }}>
        <h4 style={{ marginBottom: '20px' }}>🏆 Today's Leaderboard</h4>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {leaderboard.map((player) => (
            <div
              key={player.rank}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px',
                borderRadius: '12px',
                background: player.rank === 1 ? 'rgba(255, 105, 180, 0.1)' : 'rgba(255, 255, 255, 0.03)',
                border: player.rank === 1 ? '1px solid rgba(255, 105, 180, 0.2)' : '1px solid rgba(255, 255, 255, 0.06)'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', minWidth: '60px' }}>
                <span style={{ fontSize: '1.1rem', fontWeight: '700' }}>
                  {player.badge || `#${player.rank}`}
                </span>
                {player.rank <= 3 && (
                  <Monster size="sm" baseColor="var(--lm-pink)" accentColor="var(--lm-purple)" />
                )}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: '600', color: '#ffffff' }}>{player.name}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--muted)' }}>{player.score} XP</div>
              </div>
              {player.rank === 1 && (
                <div style={{ 
                  padding: '4px 8px', 
                  background: 'var(--lm-pink)', 
                  borderRadius: '12px', 
                  fontSize: '0.75rem',
                  fontWeight: '600',
                  color: 'white'
                }}>
                  Top Player
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Rewards Info */}
      <div className="widget-card" style={{ marginTop: '30px' }}>
        <div style={{ display: 'flex', alignItems: 'start', gap: '16px' }}>
          <div style={{ fontSize: '2rem' }}>🪙</div>
          <div style={{ flex: 1 }}>
            <h4 style={{ marginBottom: '8px' }}>Earn LM Coins</h4>
            <p style={{ color: 'var(--muted)', marginBottom: '12px', fontSize: '0.9rem' }}>
              Play games and answer questions to earn coins. Use them to customize your monster!
            </p>
            <ul style={{ 
              listStyle: 'none', 
              padding: 0, 
              fontSize: '0.85rem', 
              color: 'var(--muted)',
              lineHeight: '1.5'
            }}>
              <li>✓ 2 Coins per correct answer</li>
              <li>✓ 10 Coins for winning a game</li>
              <li>✓ 25 Coins for daily streak bonus</li>
              <li>✓ Unlock monster accessories!</li>
            </ul>
          </div>
          <Monster 
            size="md" 
            baseColor="var(--lm-pink)" 
            accentColor="var(--lm-purple)" 
            glow="neon" 
            necklace="star"
            animate={true}
          />
        </div>
      </div>
    </div>
  )
}
