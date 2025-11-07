'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useTheme } from '@/contexts/ThemeContext'
import api from '@/lib/api'

interface Class {
  id: number
  name: string
  code?: string
  instructor?: string
  semester?: string
  color?: string
}

export default function ClassesPage() {
  const router = useRouter()
  const { themeColors } = useTheme()
  
  const [classes, setClasses] = useState<Class[]>([])
  const [loading, setLoading] = useState(true)
  const [showAddForm, setShowAddForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    instructor: '',
    semester: ''
  })
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchClasses()
  }, [])

  const fetchClasses = async () => {
    try {
      setLoading(true)
      const response = await api.get('/api/classes')
      setClasses(response.data || [])
    } catch (err) {
      console.error('Error fetching classes:', err)
      setClasses([])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSubmitting(true)

    try {
      await api.post('/api/classes', {
        ...formData,
        user_id: 1 // Placeholder
      })
      
      // Success - refresh list and close form
      await fetchClasses()
      setShowAddForm(false)
      setFormData({ name: '', code: '', instructor: '', semester: '' })
    } catch (err: any) {
      console.error('Error creating class:', err)
      setError(err.response?.data?.detail || 'Failed to create class')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = async (classId: number) => {
    if (!confirm('Are you sure you want to delete this class?')) return

    try {
      await api.delete(`/api/classes/${classId}`)
      await fetchClasses()
    } catch (err) {
      console.error('Error deleting class:', err)
      alert('Failed to delete class')
    }
  }

  if (loading) {
    return (
      <div className={`flex h-screen items-center justify-center ${themeColors.bgPrimary}`}>
        <div className="text-center">
          <div className={`text-6xl mb-4 ${themeColors.textPrimary}`}>📚</div>
          <p className={`text-lg ${themeColors.textSecondary}`}>Loading classes...</p>
        </div>
      </div>
    )
  }

  return (
    <div className={`min-h-screen ${themeColors.bgPrimary} p-6`}>
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <button
              onClick={() => router.push('/dashboard')}
              className={`text-sm ${themeColors.textSecondary} hover:${themeColors.textPrimary} mb-2`}
            >
              ← Back to Dashboard
            </button>
            <h1 className={`text-3xl font-bold ${themeColors.textPrimary}`}>
              My Classes
            </h1>
            <p className={`text-base ${themeColors.textSecondary} mt-1`}>
              Manage your classes and course materials
            </p>
          </div>
          
          <button
            onClick={() => setShowAddForm(true)}
            className={`px-4 py-2 ${themeColors.accentPrimary} text-white rounded-lg hover:opacity-90 transition-opacity font-medium`}
          >
            + Add Class
          </button>
        </div>

        {/* Add Class Form Modal */}
        {showAddForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className={`${themeColors.cardBg} rounded-lg p-6 max-w-md w-full`}>
              <h2 className={`text-xl font-bold ${themeColors.textPrimary} mb-4`}>
                Add New Class
              </h2>
              
              {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                  {error}
                </div>
              )}
              
              <form onSubmit={handleSubmit}>
                <div className="space-y-4">
                  <div>
                    <label className={`block text-sm font-medium ${themeColors.textPrimary} mb-1`}>
                      Class Name *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                      className={`w-full px-3 py-2 ${themeColors.cardBg} ${themeColors.cardBorder} border rounded-lg ${themeColors.textPrimary} focus:outline-none focus:ring-2 focus:ring-blue-500`}
                      placeholder="e.g., Introduction to Psychology"
                    />
                  </div>
                  
                  <div>
                    <label className={`block text-sm font-medium ${themeColors.textPrimary} mb-1`}>
                      Course Code
                    </label>
                    <input
                      type="text"
                      value={formData.code}
                      onChange={(e) => setFormData({...formData, code: e.target.value})}
                      className={`w-full px-3 py-2 ${themeColors.cardBg} ${themeColors.cardBorder} border rounded-lg ${themeColors.textPrimary} focus:outline-none focus:ring-2 focus:ring-blue-500`}
                      placeholder="e.g., PSY 101"
                    />
                  </div>
                  
                  <div>
                    <label className={`block text-sm font-medium ${themeColors.textPrimary} mb-1`}>
                      Instructor
                    </label>
                    <input
                      type="text"
                      value={formData.instructor}
                      onChange={(e) => setFormData({...formData, instructor: e.target.value})}
                      className={`w-full px-3 py-2 ${themeColors.cardBg} ${themeColors.cardBorder} border rounded-lg ${themeColors.textPrimary} focus:outline-none focus:ring-2 focus:ring-blue-500`}
                      placeholder="e.g., Dr. Smith"
                    />
                  </div>
                  
                  <div>
                    <label className={`block text-sm font-medium ${themeColors.textPrimary} mb-1`}>
                      Semester
                    </label>
                    <input
                      type="text"
                      value={formData.semester}
                      onChange={(e) => setFormData({...formData, semester: e.target.value})}
                      className={`w-full px-3 py-2 ${themeColors.cardBg} ${themeColors.cardBorder} border rounded-lg ${themeColors.textPrimary} focus:outline-none focus:ring-2 focus:ring-blue-500`}
                      placeholder="e.g., Fall 2024"
                    />
                  </div>
                </div>
                
                <div className="flex gap-3 mt-6">
                  <button
                    type="button"
                    onClick={() => {
                      setShowAddForm(false)
                      setError('')
                      setFormData({ name: '', code: '', instructor: '', semester: '' })
                    }}
                    className={`flex-1 px-4 py-2 ${themeColors.cardBorder} border ${themeColors.textPrimary} rounded-lg hover:${themeColors.bgTertiary} transition-colors`}
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={submitting}
                    className={`flex-1 px-4 py-2 ${themeColors.accentPrimary} text-white rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50`}
                  >
                    {submitting ? 'Creating...' : 'Create Class'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Classes Grid */}
        {classes.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {classes.map((cls, index) => (
              <div
                key={cls.id}
                className={`${themeColors.cardBg} ${themeColors.cardBorder} border rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer`}
                onClick={() => router.push(`/dashboard/classes/${cls.id}`)}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className={`w-12 h-12 rounded-lg ${['bg-blue-600', 'bg-purple-600', 'bg-green-600', 'bg-red-600', 'bg-yellow-600', 'bg-indigo-600'][index % 6]} flex items-center justify-center text-white font-bold text-lg`}>
                    {cls.name.split(' ').length >= 2
                      ? cls.name.split(' ')[0][0] + cls.name.split(' ')[1][0]
                      : cls.name.slice(0, 2).toUpperCase()}
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleDelete(cls.id)
                    }}
                    className={`text-sm ${themeColors.textSecondary} hover:text-red-600 transition-colors`}
                  >
                    Delete
                  </button>
                </div>
                
                <h3 className={`text-lg font-bold ${themeColors.textPrimary} mb-1`}>
                  {cls.name}
                </h3>
                
                {cls.code && (
                  <p className={`text-sm ${themeColors.textSecondary} mb-2`}>
                    {cls.code}
                  </p>
                )}
                
                {cls.instructor && (
                  <p className={`text-sm ${themeColors.textSecondary}`}>
                    👤 {cls.instructor}
                  </p>
                )}
                
                {cls.semester && (
                  <p className={`text-sm ${themeColors.textSecondary}`}>
                    📅 {cls.semester}
                  </p>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className={`${themeColors.cardBg} ${themeColors.cardBorder} border rounded-lg p-12 text-center`}>
            <div className="text-6xl mb-4">📚</div>
            <h3 className={`text-xl font-bold ${themeColors.textPrimary} mb-2`}>
              No Classes Yet
            </h3>
            <p className={`${themeColors.textSecondary} mb-6`}>
              Add your first class to get started with Little Monster
            </p>
            <button
              onClick={() => setShowAddForm(true)}
              className={`px-6 py-3 ${themeColors.accentPrimary} text-white rounded-lg hover:opacity-90 transition-opacity font-medium`}
            >
              + Add Your First Class
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
