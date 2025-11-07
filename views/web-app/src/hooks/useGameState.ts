'use client'

import { useState, useEffect } from 'react'

export interface GameStats {
  xp: number
  coins: number
  level: number
  gamesWon: number
  totalGames: number
  streakDays: number
  achievements: string[]
}

export interface LeaderboardEntry {
  rank: number
  name: string
  score: number
  badge: string
  isCurrentUser?: boolean
}

export function useGameState() {
  const [stats, setStats] = useState<GameStats>({
    xp: 1247,
    coins: 89,
    level: 8,
    gamesWon: 12,
    totalGames: 18,
    streakDays: 5,
    achievements: ['First Win', 'Study Streak', 'Quick Learner']
  })

  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([
    { rank: 1, name: 'You', score: 1247, badge: '🥇', isCurrentUser: true },
    { rank: 2, name: 'Alex M.', score: 1150, badge: '🥈' },
    { rank: 3, name: 'Sam K.', score: 1089, badge: '🥉' },
    { rank: 4, name: 'Jordan P.', score: 976, badge: '' },
    { rank: 5, name: 'Casey L.', score: 845, badge: '' },
  ])

  // Load stats from localStorage on mount
  useEffect(() => {
    const savedStats = localStorage.getItem('lm-game-stats')
    if (savedStats) {
      try {
        setStats(JSON.parse(savedStats))
      } catch (error) {
        console.error('Failed to parse saved game stats:', error)
      }
    }
  }, [])

  // Save stats to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('lm-game-stats', JSON.stringify(stats))
  }, [stats])

  const addXP = (amount: number) => {
    setStats(prev => {
      const newXP = prev.xp + amount
      const newLevel = Math.floor(newXP / 200) + 1 // 200 XP per level
      
      return {
        ...prev,
        xp: newXP,
        level: newLevel
      }
    })
  }

  const addCoins = (amount: number) => {
    setStats(prev => ({
      ...prev,
      coins: prev.coins + amount
    }))
  }

  const recordGameWin = (gameType: string) => {
    setStats(prev => ({
      ...prev,
      gamesWon: prev.gamesWon + 1,
      totalGames: prev.totalGames + 1
    }))
    
    // Award XP and coins for winning
    addXP(50)
    addCoins(10)
    
    // Update leaderboard position
    setLeaderboard(prev => {
      const updated = [...prev]
      const userEntry = updated.find(entry => entry.isCurrentUser)
      if (userEntry) {
        userEntry.score = stats.xp + 50
        // Re-sort leaderboard
        updated.sort((a, b) => b.score - a.score)
        // Update ranks
        updated.forEach((entry, index) => {
          entry.rank = index + 1
          entry.badge = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : ''
        })
      }
      return updated
    })
  }

  const recordGameLoss = (gameType: string) => {
    setStats(prev => ({
      ...prev,
      totalGames: prev.totalGames + 1
    }))
    
    // Small consolation XP
    addXP(10)
  }

  const spendCoins = (amount: number): boolean => {
    if (stats.coins >= amount) {
      setStats(prev => ({
        ...prev,
        coins: prev.coins - amount
      }))
      return true
    }
    return false
  }

  return {
    stats,
    leaderboard,
    addXP,
    addCoins,
    recordGameWin,
    recordGameLoss,
    spendCoins
  }
}
