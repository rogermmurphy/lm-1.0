'use client'

import { usePathname } from 'next/navigation'
import Link from 'next/link'
import Monster from '@/components/Monster'

export default function Header() {
  const pathname = usePathname()
  
  const navItems = [
    { path: '/dashboard', label: 'Home' },
    { path: '/dashboard/library', label: 'Planner' },
    { path: '/dashboard/classes', label: 'Classes' },
    { path: '/dashboard/play', label: 'Games' },
    { path: '/dashboard/customize', label: 'Customize' },
  ]
  
  return (
    <header className="app-header">
      <div className="brand-section">
        <div className="brand-logo">
          <Monster size="sm" baseColor="#FFFFFF" accentColor="#E0E7FF" />
        </div>
        <div className="brand-name">Little Monster</div>
      </div>
      
      <nav className="nav-pills">
        {navItems.map(({ path, label }) => {
          const isActive = pathname === path
          return (
            <Link
              key={path}
              href={path}
              className={`nav-pill ${isActive ? 'active' : ''}`}
            >
              {label}
            </Link>
          )
        })}
      </nav>
      
      <div>
        <button className="cta-button">Get Started</button>
      </div>
    </header>
  )
}
