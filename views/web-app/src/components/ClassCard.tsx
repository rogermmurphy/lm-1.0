'use client'

import { useTheme } from '@/contexts/ThemeContext'

interface ClassCardProps {
  id: number
  name: string
  code?: string
  instructor?: string
  initials: string
  color: string
  isActive?: boolean
  onClick: () => void
}

export default function ClassCard({
  id,
  name,
  code,
  instructor,
  initials,
  color,
  isActive = false,
  onClick
}: ClassCardProps) {
  const { themeColors } = useTheme()

  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 p-3 rounded-lg transition-all ${
        isActive
          ? `${themeColors.accentLight} ${themeColors.borderPrimary} border-2`
          : `${themeColors.cardBg} hover:${themeColors.bgTertiary}`
      }`}
    >
      {/* Class Icon Circle */}
      <div
        className={`${color} flex items-center justify-center w-10 h-10 rounded-full flex-shrink-0`}
      >
        <span className="text-white font-bold text-lg">
          {initials}
        </span>
      </div>

      {/* Class Info */}
      <div className="flex-1 text-left min-w-0">
        <div className={`font-medium ${themeColors.textPrimary} truncate`}>
          {name}
        </div>
        {(code || instructor) && (
          <div className={`text-xs ${themeColors.textTertiary} truncate`}>
            {code && instructor ? `${code} • ${instructor}` : code || instructor}
          </div>
        )}
      </div>

      {/* Active Indicator */}
      {isActive && (
        <div className={`w-2 h-2 rounded-full ${themeColors.accentPrimary}`} />
      )}
    </button>
  )
}
