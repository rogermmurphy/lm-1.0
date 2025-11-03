'use client';

import { useState, useEffect } from 'react';
import { messages } from '@/lib/api';
import { Conversation, DirectMessage } from '@/types/notifications';
import { logger } from '@/lib/logger';

export default function MessagesPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);
  const [messageThread, setMessageThread] = useState<DirectMessage[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);

  // Fetch conversations
  const fetchConversations = async () => {
    setLoading(true);
    try {
      const response = await messages.getConversations();
      setConversations(response.data.conversations || []);
    } catch (error) {
      logger.error('MessagesPage', 'Failed to fetch conversations', error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch conversation thread
  const fetchConversation = async (userId: number) => {
    try {
      const response = await messages.getConversation(userId);
      setMessageThread(response.data.messages || []);
      
      // Mark messages as read
      const unreadIds = response.data.messages
        .filter((m: DirectMessage) => !m.read && m.recipient_id === 7) // Current user ID
        .map((m: DirectMessage) => m.id);
      
      if (unreadIds.length > 0) {
        await messages.markRead(unreadIds);
        // Update conversation unread count
        setConversations(prev =>
          prev.map(c => c.user_id === userId ? { ...c, unread_count: 0 } : c)
        );
      }
    } catch (error) {
      logger.error('MessagesPage', 'Failed to fetch conversation', error);
    }
  };

  // Send message
  const handleSendMessage = async () => {
    if (!newMessage.trim() || !selectedUserId || sending) return;

    setSending(true);
    try {
      await messages.send(selectedUserId, newMessage.trim());
      setNewMessage('');
      // Refresh conversation
      await fetchConversation(selectedUserId);
      await fetchConversations();
    } catch (error) {
      logger.error('MessagesPage', 'Failed to send message', error);
    } finally {
      setSending(false);
    }
  };

  // Select conversation
  const handleSelectConversation = (userId: number) => {
    setSelectedUserId(userId);
    fetchConversation(userId);
  };

  // Format time ago
  const timeAgo = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (seconds < 60) return 'just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
    return date.toLocaleDateString();
  };

  useEffect(() => {
    fetchConversations();
  }, []);

  const selectedConversation = conversations.find(c => c.user_id === selectedUserId);

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-sm h-[calc(100vh-12rem)] flex">
        {/* Conversations List */}
        <div className="w-1/3 border-r border-gray-200 flex flex-col">
          <div className="px-4 py-4 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Messages</h2>
          </div>

          <div className="flex-1 overflow-y-auto">
            {loading ? (
              <div className="px-4 py-8 text-center text-gray-500">
                Loading conversations...
              </div>
            ) : conversations.length === 0 ? (
              <div className="px-4 py-8 text-center text-gray-500">
                No conversations yet
              </div>
            ) : (
              conversations.map((conversation) => (
                <div
                  key={conversation.user_id}
                  onClick={() => handleSelectConversation(conversation.user_id)}
                  className={`px-4 py-3 border-b border-gray-100 cursor-pointer hover:bg-gray-50 ${
                    selectedUserId === conversation.user_id ? 'bg-blue-50' : ''
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <h3 className="text-sm font-semibold text-gray-900">
                          {conversation.username}
                        </h3>
                        {conversation.unread_count > 0 && (
                          <span className="px-2 py-0.5 text-xs font-bold text-white bg-blue-600 rounded-full">
                            {conversation.unread_count}
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-gray-600 mt-1 truncate">
                        {conversation.last_message}
                      </p>
                      <p className="text-xs text-gray-400 mt-1">
                        {timeAgo(conversation.last_message_time)}
                      </p>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Message Thread */}
        <div className="flex-1 flex flex-col">
          {selectedUserId ? (
            <>
              {/* Thread Header */}
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">
                  {selectedConversation?.username}
                </h3>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
                {messageThread.length === 0 ? (
                  <div className="text-center text-gray-500 py-8">
                    No messages yet. Start the conversation!
                  </div>
                ) : (
                  messageThread.map((message) => {
                    const isSent = message.sender_id === 7; // Current user ID
                    return (
                      <div
                        key={message.id}
                        className={`flex ${isSent ? 'justify-end' : 'justify-start'}`}
                      >
                        <div
                          className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                            isSent
                              ? 'bg-blue-600 text-white'
                              : 'bg-gray-100 text-gray-900'
                          }`}
                        >
                          <p className="text-sm">{message.content}</p>
                          <p
                            className={`text-xs mt-1 ${
                              isSent ? 'text-blue-100' : 'text-gray-500'
                            }`}
                          >
                            {timeAgo(message.created_at)}
                          </p>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>

              {/* Message Input */}
              <div className="px-6 py-4 border-t border-gray-200">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="Type a message..."
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={sending}
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={!newMessage.trim() || sending}
                    className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
                  >
                    {sending ? 'Sending...' : 'Send'}
                  </button>
                </div>
              </div>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center text-gray-500">
              <div className="text-center">
                <svg
                  className="w-16 h-16 mx-auto mb-4 text-gray-300"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                  />
                </svg>
                <p className="text-lg">Select a conversation to start messaging</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
