'use client'

import { useState, useEffect } from 'react'
import { transcription } from '@/lib/api'

export interface LibraryItem {
  id: string
  title: string
  type: 'Notes' | 'Document' | 'Presentation' | 'Audio' | 'Image' | 'Video'
  subject: string
  content: string
  fileUrl?: string
  fileName?: string
  fileSize?: number
  tags: string[]
  createdAt: Date
  updatedAt: Date
  isFavorite: boolean
}

export function useLibrary() {
  const [items, setItems] = useState<LibraryItem[]>([])
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)

  // Load items from localStorage on mount
  useEffect(() => {
    const savedItems = localStorage.getItem('lm-library-items')
    if (savedItems) {
      try {
        const parsed = JSON.parse(savedItems).map((item: any) => ({
          ...item,
          createdAt: new Date(item.createdAt),
          updatedAt: new Date(item.updatedAt)
        }))
        setItems(parsed)
      } catch (error) {
        console.error('Failed to load library items:', error)
      }
    } else {
      // Initialize with sample data
      const sampleItems: LibraryItem[] = [
        {
          id: '1',
          title: 'Linear Algebra Notes',
          type: 'Notes',
          subject: 'Mathematics',
          content: 'Vector spaces, matrices, eigenvalues and eigenvectors...',
          tags: ['algebra', 'vectors', 'matrices'],
          createdAt: new Date('2023-11-01'),
          updatedAt: new Date('2023-11-01'),
          isFavorite: false
        },
        {
          id: '2',
          title: 'Biology Presentation',
          type: 'Presentation',
          subject: 'Biology',
          content: 'Cell structure and function presentation notes',
          tags: ['cells', 'biology', 'presentation'],
          createdAt: new Date('2023-11-02'),
          updatedAt: new Date('2023-11-02'),
          isFavorite: true
        }
      ]
      setItems(sampleItems)
      localStorage.setItem('lm-library-items', JSON.stringify(sampleItems))
    }
  }, [])

  // Save items to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('lm-library-items', JSON.stringify(items))
  }, [items])

  const addItem = (item: Omit<LibraryItem, 'id' | 'createdAt' | 'updatedAt'>) => {
    const newItem: LibraryItem = {
      ...item,
      id: Date.now().toString(),
      createdAt: new Date(),
      updatedAt: new Date()
    }
    setItems(prev => [newItem, ...prev])
    return newItem
  }

  const updateItem = (id: string, updates: Partial<LibraryItem>) => {
    setItems(prev => prev.map(item => 
      item.id === id 
        ? { ...item, ...updates, updatedAt: new Date() }
        : item
    ))
  }

  const deleteItem = (id: string) => {
    setItems(prev => prev.filter(item => item.id !== id))
  }

  const toggleFavorite = (id: string) => {
    updateItem(id, { 
      isFavorite: !items.find(item => item.id === id)?.isFavorite 
    })
  }

  const uploadFile = async (file: File, subject: string = 'General') => {
    setUploading(true)
    try {
      let content = ''
      let type: LibraryItem['type'] = 'Document'

      // Determine type based on file
      if (file.type.startsWith('image/')) {
        type = 'Image'
        content = `Image file: ${file.name}`
      } else if (file.type.startsWith('audio/')) {
        type = 'Audio'
        // Try to transcribe audio files
        try {
          const transcriptionResult = await transcription.upload(file)
          content = transcriptionResult.data?.text || `Audio file: ${file.name}`
        } catch (error) {
          console.error('Transcription failed:', error)
          content = `Audio file: ${file.name} (transcription unavailable)`
        }
      } else if (file.type.includes('presentation') || file.name.includes('.ppt')) {
        type = 'Presentation'
        content = `Presentation file: ${file.name}`
      } else {
        type = 'Document'
        
        // Try to read text files
        if (file.type.startsWith('text/')) {
          try {
            content = await file.text()
          } catch (error) {
            content = `Document file: ${file.name}`
          }
        } else {
          content = `Document file: ${file.name}`
        }
      }

      // Create file URL for preview
      const fileUrl = URL.createObjectURL(file)

      const newItem = addItem({
        title: file.name.replace(/\.[^/.]+$/, ''), // Remove extension
        type,
        subject,
        content,
        fileUrl,
        fileName: file.name,
        fileSize: file.size,
        tags: [subject.toLowerCase(), type.toLowerCase()],
        isFavorite: false
      })

      return newItem
    } catch (error) {
      console.error('File upload failed:', error)
      throw error
    } finally {
      setUploading(false)
    }
  }

  const searchItems = (query: string) => {
    if (!query.trim()) return items
    
    const lowerQuery = query.toLowerCase()
    return items.filter(item => 
      item.title.toLowerCase().includes(lowerQuery) ||
      item.subject.toLowerCase().includes(lowerQuery) ||
      item.content.toLowerCase().includes(lowerQuery) ||
      item.tags.some(tag => tag.toLowerCase().includes(lowerQuery))
    )
  }

  const getItemsByType = (type: LibraryItem['type']) => {
    return items.filter(item => item.type === type)
  }

  const getItemsBySubject = (subject: string) => {
    return items.filter(item => item.subject.toLowerCase() === subject.toLowerCase())
  }

  const getFavoriteItems = () => {
    return items.filter(item => item.isFavorite)
  }

  const getStats = () => {
    return {
      total: items.length,
      notes: getItemsByType('Notes').length,
      documents: getItemsByType('Document').length,
      presentations: getItemsByType('Presentation').length,
      favorites: getFavoriteItems().length,
      audio: getItemsByType('Audio').length,
      images: getItemsByType('Image').length
    }
  }

  return {
    items,
    loading,
    uploading,
    addItem,
    updateItem,
    deleteItem,
    toggleFavorite,
    uploadFile,
    searchItems,
    getItemsByType,
    getItemsBySubject,
    getFavoriteItems,
    getStats
  }
}
