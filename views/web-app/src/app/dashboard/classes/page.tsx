'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface Class {
  id: number;
  name: string;
  teacher_name?: string;
  period?: string;
  color: string;
  subject?: string;
  current_grade?: string;
  grade_percent?: number;
  created_at: string;
  updated_at: string;
}

export default function ClassesPage() {
  const router = useRouter();
  const [classes, setClasses] = useState<Class[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newClass, setNewClass] = useState({
    name: '',
    teacher_name: '',
    period: '',
    color: '#3B82F6',
    subject: '',
    current_grade: '',
    grade_percent: undefined as number | undefined
  });

  useEffect(() => {
    fetchClasses();
  }, []);

  const fetchClasses = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8007/api/classes', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setClasses(data);
      }
    } catch (error) {
      console.error('Error fetching classes:', error);
    } finally {
      setLoading(false);
    }
  };

  const createClass = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8007/api/classes', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newClass)
      });
      
      if (response.ok) {
        setShowCreateModal(false);
        setNewClass({
          name: '',
          teacher_name: '',
          period: '',
          color: '#3B82F6',
          subject: '',
          current_grade: '',
          grade_percent: undefined
        });
        fetchClasses();
      }
    } catch (error) {
      console.error('Error creating class:', error);
    }
  };

  const deleteClass = async (id: number) => {
    if (!confirm('Delete this class?')) return;
    
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8007/api/classes/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        fetchClasses();
      }
    } catch (error) {
      console.error('Error deleting class:', error);
    }
  };

  if (loading) {
    return <div className="p-8">Loading classes...</div>;
  }

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">My Classes</h1>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          + Add Class
        </button>
      </div>

      {classes.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p>No classes yet. Click "Add Class" to get started!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {classes.map((cls) => (
            <div
              key={cls.id}
              className="border rounded-lg p-4 hover:shadow-lg transition-shadow cursor-pointer"
              style={{ borderLeftColor: cls.color, borderLeftWidth: '4px' }}
              onClick={() => router.push(`/dashboard/classes/${cls.id}`)}
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-bold text-lg">{cls.name}</h3>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteClass(cls.id);
                  }}
                  className="text-red-500 hover:text-red-700"
                >
                  ×
                </button>
              </div>
              
              {cls.teacher_name && (
                <p className="text-sm text-gray-600">Teacher: {cls.teacher_name}</p>
              )}
              
              {cls.period && (
                <p className="text-sm text-gray-600">Period: {cls.period}</p>
              )}
              
              {cls.subject && (
                <p className="text-sm text-gray-600">Subject: {cls.subject}</p>
              )}
              
              {cls.current_grade && (
                <div className="mt-2 flex items-center gap-2">
                  <span className="font-semibold">{cls.current_grade}</span>
                  {cls.grade_percent !== null && cls.grade_percent !== undefined && (
                    <span className="text-sm text-gray-600">({cls.grade_percent}%)</span>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Create Class Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4">Add New Class</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Class Name *</label>
                <input
                  type="text"
                  value={newClass.name}
                  onChange={(e) => setNewClass({...newClass, name: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  placeholder="e.g., AP Chemistry"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Teacher Name</label>
                <input
                  type="text"
                  value={newClass.teacher_name}
                  onChange={(e) => setNewClass({...newClass, teacher_name: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  placeholder="e.g., Mr. Smith"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Period</label>
                  <input
                    type="text"
                    value={newClass.period}
                    onChange={(e) => setNewClass({...newClass, period: e.target.value})}
                    className="w-full border rounded px-3 py-2"
                    placeholder="e.g., 3rd"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Color</label>
                  <input
                    type="color"
                    value={newClass.color}
                    onChange={(e) => setNewClass({...newClass, color: e.target.value})}
                    className="w-full border rounded px-3 py-2 h-10"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Subject</label>
                <select
                  value={newClass.subject}
                  onChange={(e) => setNewClass({...newClass, subject: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                >
                  <option value="">Select subject</option>
                  <option value="Math">Math</option>
                  <option value="Science">Science</option>
                  <option value="English">English</option>
                  <option value="History">History</option>
                  <option value="Foreign Language">Foreign Language</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Current Grade</label>
                  <input
                    type="text"
                    value={newClass.current_grade}
                    onChange={(e) => setNewClass({...newClass, current_grade: e.target.value})}
                    className="w-full border rounded px-3 py-2"
                    placeholder="e.g., A"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Grade %</label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={newClass.grade_percent || ''}
                    onChange={(e) => setNewClass({...newClass, grade_percent: e.target.value ? parseInt(e.target.value) : undefined})}
                    className="w-full border rounded px-3 py-2"
                    placeholder="95"
                  />
                </div>
              </div>
            </div>

            <div className="flex gap-2 mt-6">
              <button
                onClick={createClass}
                disabled={!newClass.name}
                className="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
              >
                Create Class
              </button>
              <button
                onClick={() => setShowCreateModal(false)}
                className="flex-1 bg-gray-200 px-4 py-2 rounded hover:bg-gray-300"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
