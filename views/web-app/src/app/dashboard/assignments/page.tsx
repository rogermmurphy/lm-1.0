'use client';

import { useState, useEffect } from 'react';

interface Assignment {
  id: number;
  class_id: number;
  title: string;
  type: string;
  description?: string;
  due_date: string;
  status: string;
  priority: string;
  created_at: string;
}

interface Class {
  id: number;
  name: string;
  color: string;
}

export default function AssignmentsPage() {
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [classes, setClasses] = useState<Class[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [filter, setFilter] = useState<string>('all');
  const [newAssignment, setNewAssignment] = useState({
    class_id: 0,
    title: '',
    type: 'homework',
    description: '',
    due_date: '',
    status: 'pending',
    priority: 'medium'
  });

  useEffect(() => {
    fetchData();
  }, [filter]);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      
      // Fetch classes
      const classesRes = await fetch('http://localhost:8007/api/classes', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (classesRes.ok) {
        setClasses(await classesRes.json());
      }
      
      // Fetch assignments
      const url = filter === 'all' 
        ? 'http://localhost:8007/api/assignments'
        : `http://localhost:8007/api/assignments?status_filter=${filter}`;
        
      const assignmentsRes = await fetch(url, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (assignmentsRes.ok) {
        setAssignments(await assignmentsRes.json());
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const createAssignment = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8007/api/assignments', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newAssignment)
      });
      
      if (response.ok) {
        setShowCreateModal(false);
        setNewAssignment({
          class_id: 0,
          title: '',
          type: 'homework',
          description: '',
          due_date: '',
          status: 'pending',
          priority: 'medium'
        });
        fetchData();
      }
    } catch (error) {
      console.error('Error creating assignment:', error);
    }
  };

  const updateStatus = async (id: number, newStatus: string) => {
    try {
      const token = localStorage.getItem('token');
      await fetch(`http://localhost:8007/api/assignments/${id}/status?new_status=${newStatus}`, {
        method: 'PATCH',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      fetchData();
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const deleteAssignment = async (id: number) => {
    if (!confirm('Delete this assignment?')) return;
    
    try {
      const token = localStorage.getItem('token');
      await fetch(`http://localhost:8007/api/assignments/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      fetchData();
    } catch (error) {
      console.error('Error deleting assignment:', error);
    }
  };

  const getClassColor = (classId: number) => {
    return classes.find(c => c.id === classId)?.color || '#3B82F6';
  };

  const getClassName = (classId: number) => {
    return classes.find(c => c.id === classId)?.name || 'Unknown';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'in-progress': return 'bg-yellow-100 text-yellow-800';
      case 'overdue': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600';
      case 'medium': return 'text-yellow-600';
      default: return 'text-gray-600';
    }
  };

  if (loading) {
    return <div className="p-8">Loading assignments...</div>;
  }

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Assignments</h1>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          + Add Assignment
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-2 mb-6">
        {['all', 'pending', 'in-progress', 'completed', 'overdue'].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded ${
              filter === f
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 hover:bg-gray-300'
            }`}
          >
            {f.charAt(0).toUpperCase() + f.slice(1).replace('-', ' ')}
          </button>
        ))}
      </div>

      {/* Assignments List */}
      {assignments.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p>No assignments found. Click "Add Assignment" to create one!</p>
        </div>
      ) : (
        <div className="space-y-4">
          {assignments.map((assignment) => (
            <div
              key={assignment.id}
              className="border rounded-lg p-4 hover:shadow-md transition-shadow"
              style={{ borderLeftColor: getClassColor(assignment.class_id), borderLeftWidth: '4px' }}
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="font-bold text-lg">{assignment.title}</h3>
                    <span className={`text-xs px-2 py-1 rounded ${getStatusColor(assignment.status)}`}>
                      {assignment.status}
                    </span>
                    <span className={`text-xs ${getPriorityColor(assignment.priority)}`}>
                      {assignment.priority} priority
                    </span>
                  </div>
                  
                  <p className="text-sm text-gray-600 mb-2">
                    Class: {getClassName(assignment.class_id)} | Type: {assignment.type}
                  </p>
                  
                  {assignment.description && (
                    <p className="text-sm text-gray-700 mb-2">{assignment.description}</p>
                  )}
                  
                  <p className="text-sm text-gray-600">
                    Due: {new Date(assignment.due_date).toLocaleString()}
                  </p>
                </div>

                <div className="flex gap-2">
                  {assignment.status !== 'completed' && (
                    <button
                      onClick={() => updateStatus(assignment.id, 'completed')}
                      className="text-green-600 hover:text-green-800 text-sm"
                    >
                      ✓ Complete
                    </button>
                  )}
                  <button
                    onClick={() => deleteAssignment(assignment.id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    ×
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Assignment Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">Add New Assignment</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Class *</label>
                <select
                  value={newAssignment.class_id}
                  onChange={(e) => setNewAssignment({...newAssignment, class_id: parseInt(e.target.value)})}
                  className="w-full border rounded px-3 py-2"
                >
                  <option value={0}>Select a class</option>
                  {classes.map((cls) => (
                    <option key={cls.id} value={cls.id}>{cls.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Title *</label>
                <input
                  type="text"
                  value={newAssignment.title}
                  onChange={(e) => setNewAssignment({...newAssignment, title: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  placeholder="e.g., Chapter 5 Homework"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Type</label>
                <select
                  value={newAssignment.type}
                  onChange={(e) => setNewAssignment({...newAssignment, type: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                >
                  <option value="homework">Homework</option>
                  <option value="project">Project</option>
                  <option value="exam">Exam</option>
                  <option value="quiz">Quiz</option>
                  <option value="reading">Reading</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <textarea
                  value={newAssignment.description}
                  onChange={(e) => setNewAssignment({...newAssignment, description: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  rows={3}
                  placeholder="Assignment details..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Due Date *</label>
                <input
                  type="datetime-local"
                  value={newAssignment.due_date}
                  onChange={(e) => setNewAssignment({...newAssignment, due_date: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Priority</label>
                <select
                  value={newAssignment.priority}
                  onChange={(e) => setNewAssignment({...newAssignment, priority: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>

            <div className="flex gap-2 mt-6">
              <button
                onClick={createAssignment}
                disabled={!newAssignment.title || !newAssignment.class_id || !newAssignment.due_date}
                className="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
              >
                Create Assignment
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
