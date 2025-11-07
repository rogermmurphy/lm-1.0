'use client';

import { useTheme } from '@/contexts/ThemeContext';

export default function ThemeSwitcher() {
  const { currentTheme, setTheme, availableThemes, themeColors } = useTheme();

  return (
    <div className={`${themeColors.cardBg} rounded-2xl shadow-xl border-2 ${themeColors.cardBorder} p-6`}>
      <h2 className={`text-2xl font-bold ${themeColors.textPrimary} mb-4`}>Theme Settings</h2>
      <p className={`${themeColors.textSecondary} mb-6`}>
        Choose your preferred color scheme for the dashboard
      </p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {availableThemes.map((theme) => (
          <button
            key={theme.name}
            onClick={() => setTheme(theme.name)}
            className={`
              p-6 rounded-xl border-2 transition-all
              ${currentTheme === theme.name 
                ? `${theme.cardBorder} ${theme.accentLight} shadow-lg` 
                : `${themeColors.cardBorder} ${themeColors.cardBg} hover:shadow-lg`
              }
            `}
          >
            <div className="text-center">
              <div className="text-4xl mb-3">{theme.icon}</div>
              <h3 className={`font-bold ${currentTheme === theme.name ? theme.textPrimary : themeColors.textPrimary}`}>
                {theme.displayName}
              </h3>
              {currentTheme === theme.name && (
                <div className={`mt-2 text-xs font-semibold ${theme.success} ${theme.successBg} px-3 py-1 rounded-full inline-block`}>
                  Active
                </div>
              )}
            </div>
          </button>
        ))}
      </div>
      
      <div className={`mt-6 p-4 ${themeColors.infoBg} border-2 ${themeColors.borderPrimary} rounded-xl`}>
        <p className={`text-sm ${themeColors.info}`}>
          <strong>Note:</strong> Your theme preference is saved automatically and will persist across sessions.
        </p>
      </div>
    </div>
  );
}
