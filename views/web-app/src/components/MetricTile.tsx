'use client'

import { ReactNode } from 'react'
import { useTheme } from '@/contexts/ThemeContext'

interface MetricTileProps {
  title: string
  value: string | number
  icon: ReactNode
  trend?: string
  subtitle?: string
  color: 'blue' | 'green' | 'purple' | 'red'
}

const colorClasses = {
  blue: {
    icon: 'bg-blue-100',
    iconColor: 'text-blue-600',
    value: 'text-blue-600',
    trend: 'text-blue-500'
  },
  green: {
    icon: 'bg-green-100',
    iconColor: 'text-green-600',
    value: 'text-green-600',
    trend: 'text-green-500'
  },
  purple: {
    icon: 'bg-purple-100',
    iconColor: 'text-purple-600',
    value: 'text-purple-600',
    trend: 'text-purple-500'
  },
  red: {
    icon: 'bg-red-100',
    iconColor: 'text-red-600',
    value: 'text-red-600',
    trend: 'text-red-500'
  }
}

export default function MetricTile({ 
  title, 
  value, 
  icon, 
  trend, 
  subtitle, 
  color 
}: MetricTileProps) {
  const { themeColors } = useTheme()
  const colors = colorClasses[color]

  return (
    <div className={`${themeColors.cardBg} ${themeColors.cardBorder} border rounded-lg p-6 hover:shadow-lg transition-shadow`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className={`text-sm font-medium ${themeColors.textSecondary} mb-1`}>
            {title}
          </p>
          <div className="flex items-baseline gap-2">
            <h3 className={`text-3xl font-bold ${colors.value}`}>
              {value}
            </h3>
            {trend && (
              <span className={`text-sm font-medium ${colors.trend}`}>
                {trend}
              </span>
            )}
          </div>
          {subtitle && (
            <p className={`text-xs ${themeColors.textTertiary} mt-1`}>
              {subtitle}
            </p>
          )}
        </div>
        <div className={`${colors.icon} ${colors.iconColor} p-3 rounded-lg`}>
          {icon}
        </div>
      </div>
    </div>
  )
}
