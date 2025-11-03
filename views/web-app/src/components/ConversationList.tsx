'use client';

import { useEffect, useState } from 'react';
import { chat } from '@/lib/api';
import { Conversation } from '@/types/chat';
import { logger } from '@/lib/logger';

interface ConversationListProps {
  selectedConversationId: number | null;
  onSelectConversation: (conversationId: number) => void;
  onNewConversation: () => void;
}

export default function ConversationList({
  selectedConversationId,
  onSelectConversation,
  onNewConversation,
}: ConversationListProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState('');

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await chat.getConversations();
      setConversations(response.data);
      logger.info('ConversationList', 'Loaded conversations', { count: response.data.length });
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to load conversations';
      setError(errorMsg);
      logger.error('ConversationList', 'Failed to load conversations', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (conversationId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    
    if (!confirm('Are you sure you want to delete this conversation? This cannot be undone.')) {
      return;
    }

    try {
      await chat.deleteConversation(conversationId);
      logger.info('ConversationList', 'Deleted conversation', { conversationId });
      
      // Remove from list
      setConversations(prev => prev.filter(c => c.id !== conversationId));
      
      // If deleted conversation was selected, clear selection
      if (selectedConversationId === conversationId) {
        onNewConversation();
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to delete conversation';
      alert(`Error: ${errorMsg}`);
      logger.error('ConversationList', 'Failed to delete conversation', err);
    }
  };

  const handleStartEdit = (conversation: Conversation, e: React.MouseEvent) => {
    e.stopPropagation();
    setEditingId(conversation.id);
    setEditTitle(conversation.title || 'Untitled');
  };

  const handleSaveEdit = async (conversationId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    
    if (!editTitle.trim()) {
      alert('Title cannot be empty');
      return;
    }

    try {
      const response = await chat.updateConversation(conversationId, editTitle.trim());
      logger.info('ConversationList', 'Updated conversation', { conversationId, newTitle: editTitle });
      
      // Update in list
      setConversations(prev => prev.map(c => 
        c.id === conversationId ? response.data : c
      ));
      
      setEditingId(null);
      setEditTitle('');
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to update conversation';
      alert(`Error: ${errorMsg}`);
      logger.error('ConversationList', 'Failed to update conversation', err);
    }
  };

  const handleCancelEdit = (e: React.MouseEvent) => {
    e.stopPropagation();
    setEditingId(null);
    setEditTitle('');
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="w-64 bg-gray-50 border-r border-gray-200 p-4">
        <div className="animate-pulse space-y-4">
          <div className="h-10 bg-gray-200 rounded"></div>
          <div className="space-y-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-16 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-64 bg-gray-50 border-r border-gray-200 flex flex-col h-full">
      {/* Header with New Conversation button */}
      <div className="p-4 border-b border-gray-200">
        <button
          onClick={onNewConversation}
          className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          + New Conversation
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto p-2">
        {error && (
          <div className="mx-2 mb-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        {conversations.length === 0 ? (
          <div className="text-center py-8 px-4 text-gray-500 text-sm">
            No conversations yet.
            <br />
            Start a new one!
          </div>
        ) : (
          <div className="space-y-1">
            {conversations.map(conversation => (
              <div
                key={conversation.id}
                onClick={() => onSelectConversation(conversation.id)}
                className={`
                  p-3 rounded-lg cursor-pointer transition-all
                  ${selectedConversationId === conversation.id
                    ? 'bg-blue-100 border-2 border-blue-500'
                    : 'bg-white hover:bg-gray-100 border-2 border-transparent'
                  }
                `}
              >
                {editingId === conversation.id ? (
                  /* Edit Mode */
                  <div className="space-y-2" onClick={e => e.stopPropagation()}>
                    <input
                      type="text"
                      value={editTitle}
                      onChange={e => setEditTitle(e.target.value)}
                      className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:border-blue-500"
                      autoFocus
                      onKeyDown={e => {
                        if (e.key === 'Enter') handleSaveEdit(conversation.id, e as any);
                        if (e.key === 'Escape') handleCancelEdit(e as any);
                      }}
                    />
                    <div className="flex gap-1">
                      <button
                        onClick={(e) => handleSaveEdit(conversation.id, e)}
                        className="flex-1 px-2 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700"
                      >
                        Save
                      </button>
                      <button
                        onClick={handleCancelEdit}
                        className="flex-1 px-2 py-1 text-xs bg-gray-500 text-white rounded hover:bg-gray-600"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  /* Display Mode */
                  <>
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1 min-w-0">
                        <h3 className="text-sm font-medium text-gray-900 truncate">
                          {conversation.title || 'Untitled Conversation'}
                        </h3>
                        <div className="flex items-center gap-2 text-xs text-gray-500 mt-1">
                          <span>{conversation.message_count} messages</span>
                          <span>•</span>
                          <span>{formatDate(conversation.updated_at)}</span>
                        </div>
                      </div>
                      
                      {/* Action buttons */}
                      <div className="flex gap-1">
                        <button
                          onClick={(e) => handleStartEdit(conversation, e)}
                          className="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                          title="Rename conversation"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                          </svg>
                        </button>
                        <button
                          onClick={(e) => handleDelete(conversation.id, e)}
                          className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                          title="Delete conversation"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer with refresh button */}
      <div className="p-4 border-t border-gray-200">
        <button
          onClick={loadConversations}
          className="w-full text-sm text-gray-600 hover:text-gray-900 transition-colors"
        >
          🔄 Refresh
        </button>
      </div>
    </div>
  );
}
