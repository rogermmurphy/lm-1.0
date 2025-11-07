'use client'

interface MonsterProps {
  size?: 'sm' | 'md' | 'lg' | 'xl'
  baseColor?: string
  accentColor?: string
  glow?: 'none' | 'soft' | 'neon'
  necklace?: 'heart' | 'star' | 'bolt' | 'initials' | 'none'
  className?: string
  animate?: boolean
}

export default function Monster({
  size = 'md',
  baseColor = '#FF69B4',
  accentColor = '#F06292',
  glow = 'none',
  necklace = 'none',
  className = '',
  animate = false
}: MonsterProps) {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-16 h-16',
    lg: 'w-24 h-24',
    xl: 'w-32 h-32'
  }

  const getNecklaceIcon = () => {
    switch (necklace) {
      case 'heart': return '❤️'
      case 'star': return '⭐'
      case 'bolt': return '⚡'
      case 'initials': return 'LM'
      default: return null
    }
  }

  const glowStyle = {
    none: {},
    soft: { 
      boxShadow: `0 0 1rem ${baseColor}66`,
      filter: 'drop-shadow(0 0 0.5rem rgba(255, 105, 180, 0.4))'
    },
    neon: { 
      boxShadow: `0 0 2rem ${baseColor}99`,
      filter: 'drop-shadow(0 0 1rem rgba(255, 105, 180, 0.8))'
    }
  }

  return (
    <div className={`relative inline-block ${className}`}>
      {/* Monster SVG */}
      <div 
        className={`${sizeClasses[size]} ${animate ? 'animate-bounce' : ''} transition-all duration-300`}
        style={glowStyle[glow]}
      >
        <svg viewBox="0 0 200 200" className="w-full h-full">
          {/* Monster Body */}
          <ellipse cx="100" cy="130" rx="60" ry="45" fill={baseColor} stroke={accentColor} strokeWidth="2"/>
          
          {/* Monster Head */}
          <circle cx="100" cy="85" r="45" fill={baseColor} stroke={accentColor} strokeWidth="2"/>
          
          {/* Fur texture */}
          <g fill={accentColor} opacity="0.6">
            <circle cx="85" cy="75" r="3"/>
            <circle cx="95" cy="65" r="2"/>
            <circle cx="105" cy="68" r="2.5"/>
            <circle cx="115" cy="78" r="2"/>
            <circle cx="75" cy="85" r="2"/>
            <circle cx="125" cy="88" r="2.5"/>
            <circle cx="90" cy="95" r="2"/>
            <circle cx="110" cy="98" r="2"/>
          </g>
          
          {/* Left Horn */}
          <path d="M 75 55 Q 70 45 65 35" stroke={accentColor} strokeWidth="4" fill="none" strokeLinecap="round"/>
          
          {/* Right Horn */}
          <path d="M 125 55 Q 130 45 135 35" stroke={accentColor} strokeWidth="4" fill="none" strokeLinecap="round"/>
          
          {/* Eyes */}
          <circle cx="88" cy="80" r="12" fill="white"/>
          <circle cx="112" cy="80" r="12" fill="white"/>
          <circle cx="88" cy="80" r="8" fill="black"/>
          <circle cx="112" cy="80" r="8" fill="black"/>
          <circle cx="90" cy="77" r="3" fill="white"/>
          <circle cx="114" cy="77" r="3" fill="white"/>
          
          {/* Mouth */}
          <path d="M 85 95 Q 100 105 115 95" stroke="#8E0E3E" strokeWidth="3" fill="#FF1744" strokeLinecap="round"/>
          <path d="M 88 98 Q 100 103 112 98" stroke="#FF8A80" strokeWidth="2" fill="none" strokeLinecap="round"/>
          
          {/* Arms */}
          <ellipse cx="55" cy="115" rx="12" ry="20" fill={baseColor} stroke={accentColor} strokeWidth="2"/>
          <ellipse cx="145" cy="115" rx="12" ry="20" fill={baseColor} stroke={accentColor} strokeWidth="2"/>
          
          {/* Feet */}
          <ellipse cx="80" cy="165" rx="15" ry="8" fill={baseColor} stroke={accentColor} strokeWidth="2"/>
          <ellipse cx="120" cy="165" rx="15" ry="8" fill={baseColor} stroke={accentColor} strokeWidth="2"/>
          
          {/* Eyebrows (happy expression) */}
          <path d="M 78 68 Q 88 65 98 68" stroke={accentColor} strokeWidth="2" fill="none" strokeLinecap="round"/>
          <path d="M 102 68 Q 112 65 122 68" stroke={accentColor} strokeWidth="2" fill="none" strokeLinecap="round"/>
        </svg>
      </div>
      
      {/* Necklace */}
      {necklace !== 'none' && (
        <div className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 text-lg">
          {getNecklaceIcon()}
        </div>
      )}
    </div>
  )
}
