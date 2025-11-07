'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export type ThemeName = 'bright' | 'dark' | 'highcontrast' | 'pink' | 'lightblue';

interface ThemeColors {
  name: ThemeName;
  displayName: string;
  icon: string;
  // Background colors
  bgPrimary: string;
  bgSecondary: string;
  bgTertiary: string;
  // Text colors
  textPrimary: string;
  textSecondary: string;
  textTertiary: string;
  // Border colors
  borderPrimary: string;
  borderSecondary: string;
  // Accent/Primary colors
  accentPrimary: string;
  accentHover: string;
  accentLight: string;
  // Component specific
  cardBg: string;
  cardBorder: string;
  sidebarBg: string;
  navBg: string;
  // Status colors
  success: string;
  successBg: string;
  error: string;
  errorBg: string;
  warning: string;
  warningBg: string;
  info: string;
  infoBg: string;
}

const themes: Record<ThemeName, ThemeColors> = {
  bright: {
    name: 'bright',
    displayName: 'Bright',
    icon: '☀️',
    bgPrimary: 'bg-gray-50',
    bgSecondary: 'bg-white',
    bgTertiary: 'bg-gray-100',
    textPrimary: 'text-gray-900',
    textSecondary: 'text-gray-600',
    textTertiary: 'text-gray-500',
    borderPrimary: 'border-gray-200',
    borderSecondary: 'border-gray-100',
    accentPrimary: 'bg-blue-600 text-white',
    accentHover: 'hover:bg-blue-700',
    accentLight: 'bg-blue-50 text-blue-600 border-blue-200',
    cardBg: 'bg-white',
    cardBorder: 'border-gray-100',
    sidebarBg: 'bg-white',
    navBg: 'bg-white',
    success: 'text-green-600',
    successBg: 'bg-green-100',
    error: 'text-red-600',
    errorBg: 'bg-red-100',
    warning: 'text-orange-600',
    warningBg: 'bg-orange-100',
    info: 'text-blue-600',
    infoBg: 'bg-blue-100',
  },
  dark: {
    name: 'dark',
    displayName: 'Dark',
    icon: '🌙',
    bgPrimary: 'bg-gray-900',
    bgSecondary: 'bg-gray-800',
    bgTertiary: 'bg-gray-700',
    textPrimary: 'text-gray-100',
    textSecondary: 'text-gray-300',
    textTertiary: 'text-gray-400',
    borderPrimary: 'border-gray-700',
    borderSecondary: 'border-gray-600',
    accentPrimary: 'bg-blue-500 text-white',
    accentHover: 'hover:bg-blue-600',
    accentLight: 'bg-blue-900 text-blue-400 border-blue-700',
    cardBg: 'bg-gray-800',
    cardBorder: 'border-gray-600',
    sidebarBg: 'bg-gray-800',
    navBg: 'bg-gray-800',
    success: 'text-green-400',
    successBg: 'bg-green-900',
    error: 'text-red-400',
    errorBg: 'bg-red-900',
    warning: 'text-orange-400',
    warningBg: 'bg-orange-900',
    info: 'text-blue-400',
    infoBg: 'bg-blue-900',
  },
  highcontrast: {
    name: 'highcontrast',
    displayName: 'High Contrast',
    icon: '⚫',
    bgPrimary: 'bg-black',
    bgSecondary: 'bg-white',
    bgTertiary: 'bg-yellow-400',
    textPrimary: 'text-white',
    textSecondary: 'text-black',
    textTertiary: 'text-gray-800',
    borderPrimary: 'border-white border-4',
    borderSecondary: 'border-black border-4',
    accentPrimary: 'bg-yellow-400 text-black font-black',
    accentHover: 'hover:bg-yellow-300',
    accentLight: 'bg-white text-black border-yellow-400 border-4',
    cardBg: 'bg-white',
    cardBorder: 'border-black border-4',
    sidebarBg: 'bg-black',
    navBg: 'bg-black',
    success: 'text-black font-black',
    successBg: 'bg-yellow-400',
    error: 'text-white font-black',
    errorBg: 'bg-black',
    warning: 'text-black font-black',
    warningBg: 'bg-yellow-400',
    info: 'text-black font-black',
    infoBg: 'bg-yellow-400',
  },
  pink: {
    name: 'pink',
    displayName: 'Pink',
    icon: '💗',
    bgPrimary: 'bg-pink-50',
    bgSecondary: 'bg-white',
    bgTertiary: 'bg-pink-100',
    textPrimary: 'text-pink-900',
    textSecondary: 'text-pink-700',
    textTertiary: 'text-pink-600',
    borderPrimary: 'border-pink-300',
    borderSecondary: 'border-pink-200',
    accentPrimary: 'bg-pink-600 text-white',
    accentHover: 'hover:bg-pink-700',
    accentLight: 'bg-pink-100 text-pink-600 border-pink-200',
    cardBg: 'bg-white',
    cardBorder: 'border-pink-200',
    sidebarBg: 'bg-white',
    navBg: 'bg-white',
    success: 'text-rose-600',
    successBg: 'bg-rose-100',
    error: 'text-red-700',
    errorBg: 'bg-red-100',
    warning: 'text-orange-700',
    warningBg: 'bg-orange-100',
    info: 'text-pink-600',
    infoBg: 'bg-pink-100',
  },
  lightblue: {
    name: 'lightblue',
    displayName: 'Light Blue',
    icon: '🌊',
    bgPrimary: 'bg-sky-50',
    bgSecondary: 'bg-white',
    bgTertiary: 'bg-sky-100',
    textPrimary: 'text-sky-900',
    textSecondary: 'text-sky-700',
    textTertiary: 'text-sky-600',
    borderPrimary: 'border-sky-300',
    borderSecondary: 'border-sky-200',
    accentPrimary: 'bg-sky-600 text-white',
    accentHover: 'hover:bg-sky-700',
    accentLight: 'bg-sky-100 text-sky-600 border-sky-200',
    cardBg: 'bg-white',
    cardBorder: 'border-sky-200',
    sidebarBg: 'bg-white',
    navBg: 'bg-white',
    success: 'text-cyan-600',
    successBg: 'bg-cyan-100',
    error: 'text-red-700',
    errorBg: 'bg-red-100',
    warning: 'text-orange-700',
    warningBg: 'bg-orange-100',
    info: 'text-sky-600',
    infoBg: 'bg-sky-100',
  },
};

interface ThemeContextType {
  currentTheme: ThemeName;
  themeColors: ThemeColors;
  setTheme: (theme: ThemeName) => void;
  availableThemes: ThemeColors[];
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [currentTheme, setCurrentTheme] = useState<ThemeName>('bright');

  // Load theme from localStorage on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('lm-theme') as ThemeName;
    if (savedTheme && themes[savedTheme]) {
      setCurrentTheme(savedTheme);
    }
  }, []);

  const setTheme = (theme: ThemeName) => {
    setCurrentTheme(theme);
    localStorage.setItem('lm-theme', theme);
  };

  const value: ThemeContextType = {
    currentTheme,
    themeColors: themes[currentTheme],
    setTheme,
    availableThemes: Object.values(themes),
  };

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
