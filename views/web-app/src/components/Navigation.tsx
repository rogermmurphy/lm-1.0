'use client'

import { Home, BookOpen, Gamepad2, Library, Palette, Coins, Trophy, Bell } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState, useEffect } from 'react'
import Monster from '@/components/Monster'
import { useGameState } from '@/hooks/useGameState'
import { useMonsterCustomization } from '@/hooks/useMonsterCustomization'

export default function Navigation() {
  const pathname = usePathname()
  const { stats } = useGameState()
  const { currentTheme } = useMonsterCustomization()
  const [apiStatus, setApiStatus] = useState<'connecting' | 'connected' | 'offline'>('connecting')
  const [notifications, setNotifications] = useState<string[]>([])

  // Check API connectivity
  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        // Simple health check - could be replaced with actual API ping
        const response = await fetch('/api/health', { 
          method: 'HEAD',
          signal: AbortSignal.timeout(3000)
        })
        setApiStatus(response.ok ? 'connected' : 'offline')
      } catch {
        setApiStatus('offline')
      }
    }

    checkApiStatus()
    const interval = setInterval(checkApiStatus, 30000) // Check every 30s
    return () => clearInterval(interval)
  }, [])

  // Check for achievements and notifications
  useEffect(() => {
    const newNotifications: string[] = []
    
    // Level up notification
    if (stats.level > 1 && stats.xp % 200 < 50) {
      newNotifications.push(`Level ${stats.level} reached! 🎉`)
    }
    
    // High coin balance notification
    if (stats.coins >= 100) {
      newNotifications.push('Ready to unlock premium items! 💎')
    }
    
    // Win streak notification
    if (stats.gamesWon > 0 && stats.gamesWon % 5 === 0) {
      newNotifications.push(`${stats.gamesWon} games won! 🏆`)
    }
    
    setNotifications(newNotifications)
  }, [stats])
  
  const navItems = [
    { path: '/dashboard', icon: Home, label: 'Home' },
    { path: '/dashboard/classes', icon: BookOpen, label: 'Classes' },
    { path: '/dashboard/play', icon: Gamepad2, label: 'Monster Play' },
    { path: '/dashboard/library', icon: Library, label: 'Library' },
    { path: '/dashboard/customize', icon: Palette, label: 'Customize LM' },
  ]

  const getApiStatusColor = () => {
    switch (apiStatus) {
      case 'connected': return 'text-green-600'
      case 'connecting': return 'text-yellow-600'
      case 'offline': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  const getApiStatusText = () => {
    switch (apiStatus) {
      case 'connected': return 'Online'
      case 'connecting': return 'Connecting...'
      case 'offline': return 'Offline Mode'
      default: return 'Unknown'
    }
  }
  
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <div className="flex items-center gap-3">
                <Monster 
                  size="sm" 
                  baseColor={currentTheme.baseColor} 
                  accentColor={currentTheme.accentColor}
                  glow={currentTheme.glow}
                  necklace={currentTheme.necklace}
                  animate={true} 
                />
                <h1 className="text-2xl font-bold text-blue-600">Little Monster</h1>
              </div>
            </div>
            <div className="ml-10 flex space-x-4">
              {navItems.map(({ path, icon: Icon, label }) => {
                const isActive = pathname === path
                return (
                  <Link
                    key={path}
                    href={path}
                    className={`inline-flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                      isActive
                        ? 'text-blue-600 bg-blue-50'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                    }`}
                    aria-label={`Navigate to ${label}`}
                  >
                    <Icon className="w-5 h-5 mr-2" />
                    {label}
                  </Link>
                )
              })}
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            {/* User Stats */}
            <div className="flex items-center space-x-3 text-sm">
              <div className="flex items-center gap-1 px-2 py-1 bg-yellow-50 rounded-full">
                <Coins className="w-4 h-4 text-yellow-600" />
                <span className="font-medium text-yellow-700">{stats.coins}</span>
              </div>
              
              <div className="flex items-center gap-1 px-2 py-1 bg-purple-50 rounded-full">
                <Trophy className="w-4 h-4 text-purple-600" />
                <span className="font-medium text-purple-700">Lv.{stats.level}</span>
              </div>
            </div>

            {/* Notifications */}
            {notifications.length > 0 && (
              <div className="relative">
                <button 
                  className="relative p-2 text-gray-600 hover:text-gray-900 transition-colors"
                  aria-label={`${notifications.length} notifications`}
                >
                  <Bell className="w-5 h-5" />
                  <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full text-xs flex items-center justify-center">
                    <span className="sr-only">{notifications.length} notifications</span>
                  </span>
                </button>
              </div>
            )}

            {/* API Status */}
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${
                apiStatus === 'connected' ? 'bg-green-500' : 
                apiStatus === 'connecting' ? 'bg-yellow-500 animate-pulse' : 
                'bg-red-500'
              }`} />
              <span className={`text-sm ${getApiStatusColor()}`}>
                {getApiStatusText()}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Notification Banner */}
      {notifications.length > 0 && (
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 border-t border-blue-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Bell className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-blue-800">
                  {notifications[0]}
                </span>
              </div>
              <button
                onClick={() => setNotifications([])}
                className="text-blue-600 hover:text-blue-800 text-sm"
                aria-label="Dismiss notification"
              >
                Dismiss
              </button>
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}
