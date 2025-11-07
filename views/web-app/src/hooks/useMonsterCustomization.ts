'use client'

import { useState, useEffect } from 'react'
import { useGameState } from './useGameState'

export interface MonsterTheme {
  baseColor: string
  accentColor: string
  glow: 'none' | 'soft' | 'neon'
  necklace: 'none' | 'heart' | 'star' | 'bolt' | 'initials'
  hat?: 'none' | 'crown' | 'tophat' | 'cap'
  wings?: boolean
  background?: string
}

export interface UnlockableItem {
  id: string
  name: string
  type: 'hat' | 'necklace' | 'wings' | 'color' | 'glow'
  cost: number
  icon: string
  value: string
  description: string
  unlocked: boolean
}

const DEFAULT_THEME: MonsterTheme = {
  baseColor: '#FF69B4', // var(--lm-pink)
  accentColor: '#8B5CF6', // var(--lm-purple)
  glow: 'soft',
  necklace: 'heart',
  hat: 'none',
  wings: false
}

export function useMonsterCustomization() {
  const [currentTheme, setCurrentTheme] = useState<MonsterTheme>(DEFAULT_THEME)
  const [unlockedItems, setUnlockedItems] = useState<string[]>([])
  const { stats, spendCoins } = useGameState()

  // Load saved customization on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('lm-monster-theme')
    const savedUnlocked = localStorage.getItem('lm-unlocked-items')
    
    if (savedTheme) {
      try {
        setCurrentTheme(JSON.parse(savedTheme))
      } catch (error) {
        console.error('Failed to load saved theme:', error)
      }
    }

    if (savedUnlocked) {
      try {
        setUnlockedItems(JSON.parse(savedUnlocked))
      } catch (error) {
        console.error('Failed to load unlocked items:', error)
      }
    }
  }, [])

  // Save theme whenever it changes
  useEffect(() => {
    localStorage.setItem('lm-monster-theme', JSON.stringify(currentTheme))
  }, [currentTheme])

  // Save unlocked items whenever they change
  useEffect(() => {
    localStorage.setItem('lm-unlocked-items', JSON.stringify(unlockedItems))
  }, [unlockedItems])

  const unlockableItems: UnlockableItem[] = [
    // Basic colors (always unlocked)
    {
      id: 'color-blue',
      name: 'Ocean Blue',
      type: 'color',
      cost: 0,
      icon: '🔵',
      value: '#3B82F6',
      description: 'Classic blue color',
      unlocked: true
    },
    {
      id: 'color-purple',
      name: 'Magic Purple',
      type: 'color', 
      cost: 0,
      icon: '🟣',
      value: '#8B5CF6',
      description: 'Mystical purple',
      unlocked: true
    },
    {
      id: 'color-green',
      name: 'Forest Green',
      type: 'color',
      cost: 0,
      icon: '🟢',
      value: '#10B981',
      description: 'Nature green',
      unlocked: true
    },
    {
      id: 'color-orange',
      name: 'Sunset Orange',
      type: 'color',
      cost: 0,
      icon: '🟠',
      value: '#F59E0B',
      description: 'Warm orange',
      unlocked: true
    },

    // Premium colors
    {
      id: 'color-gold',
      name: 'Royal Gold',
      type: 'color',
      cost: 25,
      icon: '🟡',
      value: '#FFD700',
      description: 'Shimmering gold',
      unlocked: unlockedItems.includes('color-gold')
    },
    {
      id: 'color-silver',
      name: 'Cosmic Silver',
      type: 'color',
      cost: 25,
      icon: '⚪',
      value: '#C0C0C0',
      description: 'Metallic silver',
      unlocked: unlockedItems.includes('color-silver')
    },

    // Hats
    {
      id: 'hat-crown',
      name: 'Royal Crown',
      type: 'hat',
      cost: 50,
      icon: '👑',
      value: 'crown',
      description: 'Fit for a study king/queen',
      unlocked: unlockedItems.includes('hat-crown')
    },
    {
      id: 'hat-tophat',
      name: 'Gentleman\'s Top Hat',
      type: 'hat',
      cost: 75,
      icon: '🎩',
      value: 'tophat',
      description: 'Distinguished and classy',
      unlocked: unlockedItems.includes('hat-tophat')
    },
    {
      id: 'hat-cap',
      name: 'Study Cap',
      type: 'hat',
      cost: 30,
      icon: '🧢',
      value: 'cap',
      description: 'Casual learning vibes',
      unlocked: unlockedItems.includes('hat-cap')
    },

    // Special accessories
    {
      id: 'wings',
      name: 'Angel Wings',
      type: 'wings',
      cost: 100,
      icon: '🦋',
      value: 'true',
      description: 'Soar through your studies',
      unlocked: unlockedItems.includes('wings')
    },

    // Premium necklaces
    {
      id: 'necklace-diamond',
      name: 'Diamond Necklace',
      type: 'necklace',
      cost: 80,
      icon: '💎',
      value: 'diamond',
      description: 'Sparkles with achievement',
      unlocked: unlockedItems.includes('necklace-diamond')
    },

    // Premium glows
    {
      id: 'glow-rainbow',
      name: 'Rainbow Aura',
      type: 'glow',
      cost: 150,
      icon: '🌈',
      value: 'rainbow',
      description: 'Prismatic energy field',
      unlocked: unlockedItems.includes('glow-rainbow')
    }
  ]

  const updateTheme = (updates: Partial<MonsterTheme>) => {
    setCurrentTheme(prev => ({ ...prev, ...updates }))
  }

  const purchaseItem = (itemId: string): boolean => {
    const item = unlockableItems.find(i => i.id === itemId)
    if (!item || item.unlocked) return false
    
    if (stats.coins < item.cost) {
      return false // Not enough coins
    }

    // Spend coins
    spendCoins(item.cost)
    
    // Unlock item
    setUnlockedItems(prev => [...prev, itemId])
    
    // Auto-apply if it's the first of its type
    switch (item.type) {
      case 'hat':
        if (!currentTheme.hat || currentTheme.hat === 'none') {
          updateTheme({ hat: item.value as MonsterTheme['hat'] })
        }
        break
      case 'wings':
        updateTheme({ wings: true })
        break
      case 'necklace':
        updateTheme({ necklace: item.value as MonsterTheme['necklace'] })
        break
      case 'glow':
        updateTheme({ glow: item.value as MonsterTheme['glow'] })
        break
      case 'color':
        updateTheme({ baseColor: item.value })
        break
    }

    return true
  }

  const resetToDefault = () => {
    setCurrentTheme(DEFAULT_THEME)
  }

  const getUnlockedColors = () => {
    return unlockableItems
      .filter(item => item.type === 'color' && item.unlocked)
      .map(item => ({ name: item.name, hex: item.value }))
  }

  const getUnlockedHats = () => {
    return unlockableItems
      .filter(item => item.type === 'hat' && item.unlocked)
  }

  const getUnlockedNecklaces = () => {
    return unlockableItems
      .filter(item => item.type === 'necklace' && item.unlocked)
  }

  const getUnlockedGlows = () => {
    return unlockableItems
      .filter(item => item.type === 'glow' && item.unlocked)
  }

  const getShopItems = () => {
    return unlockableItems.filter(item => !item.unlocked && item.cost > 0)
  }

  const canAfford = (itemId: string): boolean => {
    const item = unlockableItems.find(i => i.id === itemId)
    return item ? stats.coins >= item.cost : false
  }

  return {
    currentTheme,
    unlockedItems,
    unlockableItems,
    updateTheme,
    purchaseItem,
    resetToDefault,
    getUnlockedColors,
    getUnlockedHats,
    getUnlockedNecklaces,
    getUnlockedGlows,
    getShopItems,
    canAfford,
    availableCoins: stats.coins
  }
}
