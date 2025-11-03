'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';

interface StudyGroup {
  id: number;
  name: string;
  description: string;
  class_id: number | null;
  created_by_user_id: number;
  is_active: boolean;
  max_members: number;
  created_at: string;
  updated_at: string;
  role?: string;
  joined_at?: string;
}

interface GroupMessage {
  id: number;
  group_id: number;
  user_id: number;
  message_text: string;
  is_deleted: boolean;
  created_at: string;
}

export default function StudyGroupsPage() {
  const { user } = useAuth();
  const [groups, setGroups] = useState<StudyGroup[]>([]);
  const [myGroups, setMyGroups] = useState<StudyGroup[]>([]);
  const [selectedGroup, setSelectedGroup] = useState<StudyGroup | null>(null);
  const [messages, setMessages] = useState<GroupMessage[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newGroupName, setNewGroupName] = useState('');
  const [newGroupDescription, setNewGroupDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadGroups();
    loadMyGroups();
  }, []);

  useEffect(() => {
    if (selectedGroup) {
      loadMessages(selectedGroup.id);
    }
  }, [selectedGroup]);

  const loadGroups = async () => {
    try {
      const response = await fetch('http://localhost:8010/api/groups');
      const data = await response.json();
      setGroups(data);
    } catch (err) {
      console.error('Failed to load groups:', err);
    }
  };

  const loadMyGroups = async () => {
    try {
      const response = await fetch('http://localhost:8010/api/groups/my-groups');
      const data = await response.json();
      setMyGroups(data);
    } catch (err) {
      console.error('Failed to load my groups:', err);
    }
  };

  const loadMessages = async (groupId: number) => {
    try {
      const response = await fetch(`http://localhost:8010/api/groups/${groupId}/messages`);
      const data = await response.json();
      setMessages(data.reverse()); // Show oldest first
    } catch (err) {
      console.error('Failed to load messages:', err);
    }
  };

  const createGroup = async () => {
    if (!newGroupName.trim()) {
      setError('Group name is required');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8010/api/groups', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newGroupName,
          description: newGroupDescription,
          max_members: 10
        })
      });

      if (response.ok) {
        setNewGroupName('');
        setNewGroupDescription('');
        setShowCreateModal(false);
        await loadGroups();
        await loadMyGroups();
      } else {
        setError('Failed to create group');
      }
    } catch (err) {
      setError('Error creating group');
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!selectedGroup || !newMessage.trim()) return;

    try {
      const response = await fetch(`http://localhost:8010/api/groups/${selectedGroup.id}/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message_text: newMessage })
      });

      if (response.ok) {
        setNewMessage('');
        await loadMessages(selectedGroup.id);
      }
    } catch (err) {
      console.error('Failed to send message:', err);
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Study Groups</h1>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Create Group
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* My Groups */}
        <div className="lg:col-span-1">
          <h2 className="text-xl font-semibold mb-4">My Groups</h2>
          <div className="space-y-2">
            {myGroups.map(group => (
              <div
                key={group.id}
                onClick={() => setSelectedGroup(group)}
                className={`p-4 border rounded cursor-pointer hover:bg-gray-50 ${
                  selectedGroup?.id === group.id ? 'bg-blue-50 border-blue-500' : ''
                }`}
              >
                <h3 className="font-semibold">{group.name}</h3>
                <p className="text-sm text-gray-600">{group.description}</p>
                <span className="text-xs text-gray-500">Role: {group.role}</span>
              </div>
            ))}
            {myGroups.length === 0 && (
              <p className="text-gray-500">You haven't joined any groups yet</p>
            )}
          </div>

          <h2 className="text-xl font-semibold mt-8 mb-4">All Groups</h2>
          <div className="space-y-2">
            {groups.filter(g => !myGroups.find(mg => mg.id === g.id)).map(group => (
              <div
                key={group.id}
                className="p-4 border rounded hover:bg-gray-50"
              >
                <h3 className="font-semibold">{group.name}</h3>
                <p className="text-sm text-gray-600">{group.description}</p>
                <button className="mt-2 text-sm text-blue-600 hover:underline">
                  Join Group
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Group Chat */}
        <div className="lg:col-span-2">
          {selectedGroup ? (
            <div className="border rounded-lg h-[600px] flex flex-col">
              <div className="p-4 border-b bg-gray-50">
                <h2 className="text-xl font-semibold">{selectedGroup.name}</h2>
                <p className="text-sm text-gray-600">{selectedGroup.description}</p>
              </div>

              <div className="flex-1 overflow-y-auto p-4 space-y-3">
                {messages.map(msg => (
                  <div key={msg.id} className="bg-gray-100 p-3 rounded">
                    <p className="text-sm font-semibold text-gray-700">
                      User {msg.user_id}
                    </p>
                    <p className="mt-1">{msg.message_text}</p>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(msg.created_at).toLocaleString()}
                    </p>
                  </div>
                ))}
                {messages.length === 0 && (
                  <p className="text-gray-500 text-center mt-8">
                    No messages yet. Start the conversation!
                  </p>
                )}
              </div>

              <div className="p-4 border-t">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Type a message..."
                    className="flex-1 border rounded px-3 py-2"
                  />
                  <button
                    onClick={sendMessage}
                    className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="border rounded-lg h-[600px] flex items-center justify-center text-gray-500">
              Select a group to view messages
            </div>
          )}
        </div>
      </div>

      {/* Create Group Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4">Create Study Group</h2>
            
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                {error}
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Group Name</label>
                <input
                  type="text"
                  value={newGroupName}
                  onChange={(e) => setNewGroupName(e.target.value)}
                  className="w-full border rounded px-3 py-2"
                  placeholder="e.g., Math Study Group"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <textarea
                  value={newGroupDescription}
                  onChange={(e) => setNewGroupDescription(e.target.value)}
                  className="w-full border rounded px-3 py-2"
                  rows={3}
                  placeholder="What is this group for?"
                />
              </div>

              <div className="flex gap-2 justify-end">
                <button
                  onClick={() => {
                    setShowCreateModal(false);
                    setError('');
                  }}
                  className="px-4 py-2 border rounded hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  onClick={createGroup}
                  disabled={loading}
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
                >
                  {loading ? 'Creating...' : 'Create Group'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
