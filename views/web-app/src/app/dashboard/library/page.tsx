'use client'

import { useState, useRef } from 'react'
import { useLibrary, LibraryItem } from '@/hooks/useLibrary'

export default function LibraryPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedItem, setSelectedItem] = useState<LibraryItem | null>(null)
  const [isCreating, setIsCreating] = useState(false)
  const [newItemTitle, setNewItemTitle] = useState('')
  const [newItemSubject, setNewItemSubject] = useState('General')
  const [newItemContent, setNewItemContent] = useState('')
  const [newItemType, setNewItemType] = useState<LibraryItem['type']>('Notes')
  const fileInputRef = useRef<HTMLInputElement>(null)
  
  const {
    items,
    loading,
    uploading,
    addItem,
    updateItem,
    deleteItem,
    toggleFavorite,
    uploadFile,
    searchItems,
    getStats
  } = useLibrary()

  const filteredItems = searchItems(searchTerm)
  const stats = getStats()

  const getItemIcon = (type: LibraryItem['type']) => {
    switch (type) {
      case 'Notes': return '📚'
      case 'Document': return '📝'
      case 'Presentation': return '🧬'
      case 'Audio': return '🎵'
      case 'Image': return '🖼️'
      case 'Video': return '🎥'
      default: return '📄'
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    try {
      await uploadFile(file, newItemSubject)
      alert(`${file.name} uploaded successfully!`)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    } catch (error) {
      alert('Upload failed. Please try again.')
    }
  }

  const handleCreateNew = () => {
    if (!newItemTitle.trim() || !newItemContent.trim()) {
      alert('Please fill in title and content')
      return
    }

    addItem({
      title: newItemTitle,
      type: newItemType,
      subject: newItemSubject,
      content: newItemContent,
      tags: [newItemSubject.toLowerCase(), newItemType.toLowerCase()],
      isFavorite: false
    })

    setNewItemTitle('')
    setNewItemContent('')
    setIsCreating(false)
    alert('Item created successfully!')
  }

  const handleViewItem = (item: LibraryItem) => {
    setSelectedItem(item)
  }

  const handleEditItem = (item: LibraryItem) => {
    setSelectedItem(item)
    setNewItemTitle(item.title)
    setNewItemContent(item.content)
    setNewItemSubject(item.subject)
    setNewItemType(item.type)
    setIsCreating(true)
  }

  const handleDeleteItem = (id: string) => {
    if (confirm('Are you sure you want to delete this item?')) {
      deleteItem(id)
      if (selectedItem?.id === id) {
        setSelectedItem(null)
      }
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Library 📚</h1>
        <p className="text-gray-600">Your collected notes, presentations, and study materials</p>
      </div>

      {/* Search */}
      <div className="card">
        <div className="flex gap-4">
          <input
            type="text"
            placeholder="Search your library..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button 
            onClick={() => setSearchTerm('')}
            className="px-6 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors font-medium"
          >
            {searchTerm ? 'Clear' : 'Search'}
          </button>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid md:grid-cols-6 gap-4">
        <div className="card text-center">
          <div className="text-2xl mb-2">📚</div>
          <div className="text-lg font-bold">{stats.total}</div>
          <div className="text-xs text-gray-600">Total Items</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl mb-2">📝</div>
          <div className="text-lg font-bold">{stats.notes}</div>
          <div className="text-xs text-gray-600">Notes</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl mb-2">📄</div>
          <div className="text-lg font-bold">{stats.documents}</div>
          <div className="text-xs text-gray-600">Documents</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl mb-2">🎯</div>
          <div className="text-lg font-bold">{stats.presentations}</div>
          <div className="text-xs text-gray-600">Presentations</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl mb-2">🎵</div>
          <div className="text-lg font-bold">{stats.audio}</div>
          <div className="text-xs text-gray-600">Audio</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl mb-2">⭐</div>
          <div className="text-lg font-bold">{stats.favorites}</div>
          <div className="text-xs text-gray-600">Favorites</div>
        </div>
      </div>

      {/* Library Items */}
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-semibold">
            {searchTerm ? `Search Results (${filteredItems.length})` : 'Recent Items'}
          </h2>
          {loading && <div className="text-sm text-gray-500">Loading...</div>}
        </div>
        
        <div className="grid gap-4">
          {filteredItems.length === 0 ? (
            <div className="card text-center py-8">
              <div className="text-4xl mb-4">📭</div>
              <h3 className="text-lg font-semibold mb-2">No items found</h3>
              <p className="text-gray-600">
                {searchTerm ? 'Try a different search term' : 'Start by creating your first library item!'}
              </p>
            </div>
          ) : (
            filteredItems.map((item) => (
              <div key={item.id} className="card hover:shadow-lg transition-shadow">
                <div className="flex items-center gap-4">
                  <div className="text-3xl">{getItemIcon(item.type)}</div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-lg">{item.title}</h3>
                      {item.isFavorite && <span className="text-yellow-500">⭐</span>}
                    </div>
                    <div className="flex gap-4 text-sm text-gray-600">
                      <span>{item.type}</span>
                      <span>•</span>
                      <span>{item.subject}</span>
                      <span>•</span>
                      <span>{item.createdAt.toLocaleDateString()}</span>
                      {item.fileSize && (
                        <>
                          <span>•</span>
                          <span>{Math.round(item.fileSize / 1024)} KB</span>
                        </>
                      )}
                    </div>
                    <div className="flex gap-1 mt-1">
                      {item.tags.map(tag => (
                        <span key={tag} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button 
                      onClick={() => toggleFavorite(item.id)}
                      className="p-2 text-gray-600 hover:text-yellow-500 transition-colors"
                      title={item.isFavorite ? 'Remove from favorites' : 'Add to favorites'}
                    >
                      {item.isFavorite ? '⭐' : '☆'}
                    </button>
                    <button 
                      onClick={() => handleViewItem(item)}
                      className="px-4 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-medium"
                    >
                      View
                    </button>
                    <button 
                      onClick={() => handleEditItem(item)}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                    >
                      Edit
                    </button>
                    <button 
                      onClick={() => handleDeleteItem(item.id)}
                      className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Upload New */}
      <div className="card bg-gradient-to-r from-green-50 to-blue-50 border-green-200">
        <div className="flex items-center gap-4">
          <div className="text-3xl">📤</div>
          <div className="flex-1">
            <h3 className="font-semibold mb-2">Add to Library</h3>
            <p className="text-sm text-gray-700 mb-3">
              Upload files with automatic transcription for audio, or create new content from scratch!
            </p>
            <div className="flex gap-2 flex-wrap">
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileUpload}
                accept=".txt,.pdf,.doc,.docx,.ppt,.pptx,.mp3,.wav,.m4a,.jpg,.jpeg,.png,.gif"
                className="hidden"
              />
              <button 
                onClick={() => fileInputRef.current?.click()}
                disabled={uploading}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium disabled:opacity-50"
              >
                {uploading ? 'Uploading...' : 'Upload File'}
              </button>
              <button 
                onClick={() => setIsCreating(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Create New
              </button>
              <select
                value={newItemSubject}
                onChange={(e) => setNewItemSubject(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
              >
                <option value="General">General</option>
                <option value="Mathematics">Mathematics</option>
                <option value="Science">Science</option>
                <option value="English">English</option>
                <option value="History">History</option>
                <option value="Spanish">Spanish</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Create/Edit Modal */}
      {isCreating && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl mx-4">
            <h2 className="text-xl font-bold mb-4">
              {selectedItem ? 'Edit Item' : 'Create New Item'}
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Title</label>
                <input
                  type="text"
                  value={newItemTitle}
                  onChange={(e) => setNewItemTitle(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  placeholder="Enter title..."
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Type</label>
                  <select
                    value={newItemType}
                    onChange={(e) => setNewItemType(e.target.value as LibraryItem['type'])}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  >
                    <option value="Notes">Notes</option>
                    <option value="Document">Document</option>
                    <option value="Presentation">Presentation</option>
                    <option value="Audio">Audio</option>
                    <option value="Image">Image</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Subject</label>
                  <select
                    value={newItemSubject}
                    onChange={(e) => setNewItemSubject(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  >
                    <option value="General">General</option>
                    <option value="Mathematics">Mathematics</option>
                    <option value="Science">Science</option>
                    <option value="English">English</option>
                    <option value="History">History</option>
                    <option value="Spanish">Spanish</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Content</label>
                <textarea
                  value={newItemContent}
                  onChange={(e) => setNewItemContent(e.target.value)}
                  rows={10}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg resize-none"
                  placeholder="Enter your content here..."
                />
              </div>
            </div>
            <div className="flex justify-end gap-2 mt-6">
              <button
                onClick={() => {
                  setIsCreating(false)
                  setSelectedItem(null)
                  setNewItemTitle('')
                  setNewItemContent('')
                }}
                className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (selectedItem) {
                    updateItem(selectedItem.id, {
                      title: newItemTitle,
                      content: newItemContent,
                      subject: newItemSubject,
                      type: newItemType,
                      tags: [newItemSubject.toLowerCase(), newItemType.toLowerCase()]
                    })
                    setSelectedItem(null)
                    setIsCreating(false)
                    alert('Item updated successfully!')
                  } else {
                    handleCreateNew()
                  }
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                {selectedItem ? 'Update' : 'Create'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* View Modal */}
      {selectedItem && !isCreating && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-xl font-bold">{selectedItem.title}</h2>
                <div className="text-sm text-gray-600 mt-1">
                  {selectedItem.type} • {selectedItem.subject} • {selectedItem.createdAt.toLocaleDateString()}
                </div>
              </div>
              <button
                onClick={() => setSelectedItem(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            
            {selectedItem.fileUrl && selectedItem.type === 'Image' && (
              <div className="mb-4">
                <img 
                  src={selectedItem.fileUrl} 
                  alt={selectedItem.title}
                  className="max-w-full h-auto rounded-lg"
                />
              </div>
            )}

            {selectedItem.fileUrl && selectedItem.type === 'Audio' && (
              <div className="mb-4">
                <audio controls className="w-full">
                  <source src={selectedItem.fileUrl} />
                  Your browser does not support the audio element.
                </audio>
              </div>
            )}

            <div className="bg-gray-50 rounded-lg p-4">
              <pre className="whitespace-pre-wrap font-sans text-sm">
                {selectedItem.content}
              </pre>
            </div>

            <div className="flex justify-between items-center mt-4">
              <div className="flex gap-1">
                {selectedItem.tags.map(tag => (
                  <span key={tag} className="text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded">
                    {tag}
                  </span>
                ))}
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => toggleFavorite(selectedItem.id)}
                  className="px-4 py-2 text-yellow-600 border border-yellow-600 rounded-lg hover:bg-yellow-50"
                >
                  {selectedItem.isFavorite ? 'Remove Favorite' : 'Add Favorite'}
                </button>
                <button
                  onClick={() => handleEditItem(selectedItem)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Edit
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
