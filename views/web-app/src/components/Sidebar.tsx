'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

interface NavItem {
  href: string;
  label: string;
  icon: string;
}

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuth();
  const [isPinned, setIsPinned] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  // Load pinned state from localStorage
  useEffect(() => {
    const savedPinned = localStorage.getItem('sidebarPinned');
    if (savedPinned === 'true') {
      setIsPinned(true);
    }
  }, []);

  const togglePin = () => {
    const newPinned = !isPinned;
    setIsPinned(newPinned);
    localStorage.setItem('sidebarPinned', newPinned.toString());
  };

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  const isExpanded = isPinned || isHovered;

  const navItems: NavItem[] = [
    { href: '/dashboard', label: 'Dashboard', icon: '🏠' },
    { href: '/dashboard/classes', label: 'Classes', icon: '📖' },
    { href: '/dashboard/assignments', label: 'Assignments', icon: '📝' },
    { href: '/dashboard/flashcards', label: 'Flashcards', icon: '🎴' },
    { href: '/dashboard/groups', label: 'Study Groups', icon: '👥' },
    { href: '/dashboard/messages', label: 'Messages', icon: '✉️' },
    { href: '/dashboard/notifications', label: 'Notifications', icon: '🔔' },
    { href: '/dashboard/chat', label: 'AI Chat', icon: '💬' },
    { href: '/dashboard/transcribe', label: 'Transcribe', icon: '🎤' },
    { href: '/dashboard/tts', label: 'Text-to-Speech', icon: '🔊' },
    { href: '/dashboard/materials', label: 'Materials', icon: '📚' },
    { href: '/dashboard/logs', label: 'Logs', icon: '🔍' },
  ];

  return (
    <>
      {/* Sidebar - Hidden on mobile, always visible on desktop */}
      <aside
        className={`hidden lg:block fixed left-0 top-0 h-full bg-white shadow-lg transition-all duration-300 ease-in-out z-40 ${
          isExpanded ? 'w-64' : 'w-16'
        }`}
        onMouseEnter={() => !isPinned && setIsHovered(true)}
        onMouseLeave={() => !isPinned && setIsHovered(false)}
      >
        {/* Header */}
        <div className="flex items-center justify-between h-16 px-4 border-b border-gray-200">
          <Link href="/dashboard" className="flex items-center space-x-2">
            <span className="text-2xl">🦖</span>
            {isExpanded && (
              <h1 className="text-lg font-bold text-blue-600 whitespace-nowrap">
                Little Monster
              </h1>
            )}
          </Link>
          {isExpanded && (
            <button
              onClick={togglePin}
              className="p-1 rounded hover:bg-gray-100 transition-colors"
              title={isPinned ? 'Unpin sidebar' : 'Pin sidebar'}
            >
              {isPinned ? (
                <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              ) : (
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              )}
            </button>
          )}
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 overflow-y-auto py-4">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center px-4 py-3 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-50 text-blue-700 border-r-4 border-blue-700'
                    : 'text-gray-700 hover:bg-gray-50 hover:text-blue-600'
                }`}
              >
                <span className="text-xl min-w-[24px]">{item.icon}</span>
                {isExpanded && (
                  <span className="ml-3 whitespace-nowrap">{item.label}</span>
                )}
              </Link>
            );
          })}
        </nav>

        {/* User Section */}
        <div className="border-t border-gray-200 p-4">
          {isExpanded ? (
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                  <span className="text-blue-600 font-semibold">
                    {user?.username?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || 'U'}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {user?.username || user?.email}
                  </p>
                </div>
              </div>
              <button
                onClick={handleLogout}
                className="w-full flex items-center justify-center space-x-2 bg-gray-100 text-gray-700 hover:bg-gray-200 px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                <span>🚪</span>
                <span>Logout</span>
              </button>
            </div>
          ) : (
            <div className="flex flex-col items-center space-y-3">
              <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                <span className="text-blue-600 font-semibold text-sm">
                  {user?.username?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || 'U'}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="text-xl hover:bg-gray-100 p-1 rounded transition-colors"
                title="Logout"
              >
                🚪
              </button>
            </div>
          )}
        </div>
      </aside>

      {/* Top Bar for Mobile */}
      <div className="lg:hidden fixed top-0 left-0 right-0 h-16 bg-white shadow-sm z-30 flex items-center justify-between px-4">
        <Link href="/dashboard" className="flex items-center space-x-2">
          <span className="text-2xl">🦖</span>
          <h1 className="text-lg font-bold text-blue-600">Little Monster</h1>
        </Link>
        <button
          onClick={handleLogout}
          className="bg-gray-100 text-gray-700 hover:bg-gray-200 px-3 py-1 rounded text-sm"
        >
          Logout
        </button>
      </div>

      {/* Mobile Bottom Navigation */}
      <div className="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-30">
        <div className="grid grid-cols-5 gap-1">
          {navItems.slice(0, 5).map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex flex-col items-center py-2 text-xs ${
                  isActive ? 'text-blue-700' : 'text-gray-600'
                }`}
              >
                <span className="text-xl mb-1">{item.icon}</span>
                <span className="truncate max-w-full px-1">{item.label}</span>
              </Link>
            );
          })}
        </div>
      </div>
    </>
  );
}
