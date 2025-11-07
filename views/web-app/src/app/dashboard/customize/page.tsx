'use client'

import { useState } from 'react'
import Monster from '@/components/Monster'
import { useMonsterCustomization } from '@/hooks/useMonsterCustomization'
import ThemeSwitcher from '@/components/ThemeSwitcher'

export default function CustomizeLMPage() {
  const [activeTab, setActiveTab] = useState<'customize' | 'theme' | 'shop'>('customize')
  
  const {
    currentTheme,
    updateTheme,
    purchaseItem,
    resetToDefault,
    getUnlockedColors,
    getUnlockedHats,
    getUnlockedNecklaces,
    getUnlockedGlows,
    getShopItems,
    canAfford,
    availableCoins
  } = useMonsterCustomization()

  const unlockedColors = getUnlockedColors()
  const unlockedHats = getUnlockedHats()
  const unlockedNecklaces = getUnlockedNecklaces()
  const unlockedGlows = getUnlockedGlows()
  const shopItems = getShopItems()

  const glowOptions = [
    { value: 'none', label: 'None' },
    { value: 'soft', label: 'Soft' },
    { value: 'neon', label: 'Neon' },
    ...unlockedGlows.map(item => ({
      value: item.value,
      label: item.name
    }))
  ]

  const necklaceOptions = [
    { value: 'none', label: 'None', icon: '' },
    { value: 'heart', label: 'Heart', icon: '❤️' },
    { value: 'star', label: 'Star', icon: '⭐' },
    { value: 'bolt', label: 'Bolt', icon: '⚡' },
    { value: 'initials', label: 'Initials', icon: 'LM' },
    ...unlockedNecklaces.map(item => ({
      value: item.value,
      label: item.name,
      icon: item.icon
    }))
  ]

  const hatOptions = [
    { value: 'none', label: 'None', icon: '' },
    ...unlockedHats.map(item => ({
      value: item.value,
      label: item.name,
      icon: item.icon
    }))
  ]

  const handlePurchase = (itemId: string) => {
    const success = purchaseItem(itemId)
    if (success) {
      alert('Item purchased successfully! 🎉')
    } else {
      const item = shopItems.find(i => i.id === itemId)
      if (item && availableCoins < item.cost) {
        alert(`Not enough coins! You need ${item.cost} coins but only have ${availableCoins}.`)
      } else {
        alert('Purchase failed. Please try again.')
      }
    }
  }

  return (
    <div className="space-y-8">
      {/* Header with Coin Balance */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold mb-2">Customize LM 🎨</h1>
          <p className="text-gray-600">Make LM match your style</p>
        </div>
        <div className="text-right">
          <div className="flex items-center gap-2 text-xl font-bold">
            <span>🪙</span>
            <span>{availableCoins}</span>
          </div>
          <div className="text-sm text-gray-600">LM Coins</div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex gap-2">
        <button
          onClick={() => setActiveTab('customize')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            activeTab === 'customize'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          🎨 Customize LM
        </button>
        <button
          onClick={() => setActiveTab('theme')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            activeTab === 'theme'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          🌈 Dashboard Theme
        </button>
        <button
          onClick={() => setActiveTab('shop')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            activeTab === 'shop'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          🛍️ Shop ({shopItems.length})
        </button>
      </div>

      {activeTab === 'theme' ? (
        /* Theme Tab */
        <ThemeSwitcher />
      ) : activeTab === 'customize' ? (
        <div className="grid md:grid-cols-2 gap-6">
          {/* Colors Section */}
          <div className="card">
            <h2 className="font-semibold text-lg mb-4 flex items-center gap-2">
              <span className="text-2xl">🎨</span>
              Colors
            </h2>
            
            {/* Base Color */}
            <div className="mb-6">
              <div className="text-sm text-gray-600 mb-3">Base color</div>
              <div className="flex flex-wrap gap-2">
                {unlockedColors.map((color) => (
                  <button
                    key={color.name + '-base'}
                    className={`w-10 h-10 rounded-full border-2 hover:scale-110 transition-transform ${
                      currentTheme.baseColor === color.hex ? 'ring-2 ring-offset-2 ring-gray-400' : 'border-gray-200'
                    }`}
                    style={{ backgroundColor: color.hex }}
                    title={color.name}
                    onClick={() => updateTheme({ baseColor: color.hex })}
                  />
                ))}
              </div>
            </div>

            {/* Accent Color */}
            <div>
              <div className="text-sm text-gray-600 mb-3">Accent color</div>
              <div className="flex flex-wrap gap-2">
                {unlockedColors.map((color) => (
                  <button
                    key={color.name + '-accent'}
                    className={`w-10 h-10 rounded-full border-2 hover:scale-110 transition-transform ${
                      currentTheme.accentColor === color.hex ? 'ring-2 ring-offset-2 ring-gray-400' : 'border-gray-200'
                    }`}
                    style={{ backgroundColor: color.hex }}
                    title={color.name}
                    onClick={() => updateTheme({ accentColor: color.hex })}
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Style Section */}
          <div className="card">
            <h2 className="font-semibold text-lg mb-4 flex items-center gap-2">
              <span className="text-2xl">✨</span>
              Style & Accessories
            </h2>
            
            {/* Glow Effect */}
            <div className="mb-6">
              <div className="text-sm text-gray-600 mb-3">Glow effect</div>
              <div className="grid grid-cols-3 gap-2">
                {glowOptions.map((option) => (
                  <button
                    key={option.value}
                    className={`px-3 py-2 rounded-lg border-2 transition-all text-sm ${
                      currentTheme.glow === option.value
                        ? 'border-blue-600 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => updateTheme({ glow: option.value as any })}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Necklace */}
            <div className="mb-6">
              <div className="text-sm text-gray-600 mb-3">Necklace accessory</div>
              <div className="grid grid-cols-3 gap-2">
                {necklaceOptions.map((option) => (
                  <button
                    key={option.value}
                    className={`px-2 py-3 rounded-lg border-2 transition-all text-center ${
                      currentTheme.necklace === option.value
                        ? 'border-blue-600 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => updateTheme({ necklace: option.value as any })}
                  >
                    <div className="text-xl mb-1">{option.icon}</div>
                    <div className="font-medium text-xs">{option.label}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Hat */}
            {hatOptions.length > 1 && (
              <div className="mb-6">
                <div className="text-sm text-gray-600 mb-3">Hat</div>
                <div className="grid grid-cols-3 gap-2">
                  {hatOptions.map((option) => (
                    <button
                      key={option.value}
                      className={`px-2 py-3 rounded-lg border-2 transition-all text-center ${
                        currentTheme.hat === option.value
                          ? 'border-blue-600 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                      onClick={() => updateTheme({ hat: option.value as any })}
                    >
                      <div className="text-xl mb-1">{option.icon}</div>
                      <div className="font-medium text-xs">{option.label}</div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Preview Section */}
          <div className="card md:col-span-2">
            <h2 className="font-semibold text-lg mb-4">Live Preview</h2>
            <div className="rounded-2xl p-8 bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col md:flex-row items-center justify-center gap-8">
              <Monster 
                size="lg"
                baseColor={currentTheme.baseColor}
                accentColor={currentTheme.accentColor}
                glow={currentTheme.glow}
                necklace={currentTheme.necklace}
                animate={true}
              />
              <div className="text-center">
                <div className="text-lg font-medium mb-2">✨ LM says:</div>
                <div className="text-gray-600 italic text-lg">
                  &quot;I love my new look! Thanks for making me unique! 💖&quot;
                </div>
                <div className="mt-4 flex gap-2 justify-center">
                  <button
                    onClick={resetToDefault}
                    className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 text-sm"
                  >
                    Reset to Default
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        /* Shop Tab */
        <div className="space-y-6">
          {shopItems.length === 0 ? (
            <div className="card text-center py-12">
              <div className="text-4xl mb-4">🎉</div>
              <h3 className="text-xl font-bold mb-2">All Items Unlocked!</h3>
              <p className="text-gray-600">
                Congratulations! You've unlocked all available customization items.
              </p>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {shopItems.map((item) => (
                <div key={item.id} className="card">
                  <div className="text-center">
                    <div className="text-4xl mb-3">{item.icon}</div>
                    <h3 className="font-bold text-lg mb-1">{item.name}</h3>
                    <p className="text-sm text-gray-600 mb-3">{item.description}</p>
                    <div className="flex items-center justify-center gap-1 mb-4">
                      <span className="text-xl">🪙</span>
                      <span className="text-xl font-bold">{item.cost}</span>
                    </div>
                    <button
                      onClick={() => handlePurchase(item.id)}
                      disabled={!canAfford(item.id)}
                      className={`w-full py-2 px-4 rounded-lg font-medium transition-colors ${
                        canAfford(item.id)
                          ? 'bg-green-600 text-white hover:bg-green-700'
                          : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                      }`}
                    >
                      {canAfford(item.id) ? 'Purchase' : 'Not Enough Coins'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
          
          {shopItems.length > 0 && (
            <div className="card bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
              <div className="flex items-center gap-4">
                <div className="text-3xl">🎮</div>
                <div className="flex-1">
                  <h3 className="font-semibold mb-2">Need More Coins?</h3>
                  <p className="text-sm text-gray-700 mb-3">
                    Play games to earn LM Coins! Snake, Tic-Tac-Toe, and Quiz Arena all reward coins for playing.
                  </p>
                  <button
                    onClick={() => window.open('/dashboard/play', '_blank')}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
                  >
                    Go Play Games
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
