/**
 * API Client for Little Monster Backend
 * Connects to API Gateway at http://localhost
 */
import axios from 'axios';
import { logger } from './logger';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost';

logger.info('API', 'API Client initializing', { baseURL: API_URL });

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token and log requests
api.interceptors.request.use(
  (config) => {
    logger.debug('API Request', `${config.method?.toUpperCase()} ${config.url}`, {
      headers: config.headers,
      data: config.data,
      params: config.params
    });
    
    // Don't add token for auth endpoints
    if (config.url?.includes('/api/auth/')) {
      logger.debug('API Request', 'Skipping token for auth endpoint');
      return config;
    }
    
    // Get token from localStorage
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('accessToken');  // Fixed: was 'access_token'
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
        logger.debug('API Request', 'Added JWT token to request');
      } else {
        logger.warn('API Request', 'No JWT token found in localStorage');
      }
    }
    
    return config;
  },
  (error) => {
    logger.error('API Request', 'Request interceptor error', error);
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh and log responses
api.interceptors.response.use(
  (response) => {
    logger.debug('API Response', `${response.status} ${response.config.url}`, {
      status: response.status,
      statusText: response.statusText,
      data: response.data,
      headers: response.headers
    });
    return response;
  },
  async (error) => {
    logger.error('API Response', `Error: ${error.response?.status || 'Network'} ${error.config?.url}`, {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      message: error.message
    });
    
    const originalRequest = error.config;
    
    // If 401 and not already retrying, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      if (typeof window !== 'undefined') {
        const refreshToken = localStorage.getItem('refreshToken');  // Fixed: was 'refresh_token'
        
        if (refreshToken) {
          try {
            const response = await axios.post(`${API_URL}/api/auth/refresh`, {
              refresh_token: refreshToken,
            });
            
            const { access_token } = response.data;
            localStorage.setItem('accessToken', access_token);  // Fixed: was 'access_token'
            
            // Retry original request with new token
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
            return axios(originalRequest);
          } catch (refreshError) {
            // Refresh failed, clear tokens and redirect to login
            localStorage.removeItem('accessToken');  // Fixed: was 'access_token'
            localStorage.removeItem('refreshToken');  // Fixed: was 'refresh_token'
            localStorage.removeItem('user');
            if (typeof window !== 'undefined') {
              window.location.href = '/login';
            }
            return Promise.reject(refreshError);
          }
        }
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const auth = {
  register: (email: string, password: string, username?: string) =>
    api.post('/api/auth/register', { email, password, username }),
  
  login: (email: string, password: string) =>
    api.post('/api/auth/login', { email, password }),
  
  logout: (refreshToken: string) =>
    api.post('/api/auth/logout', { refresh_token: refreshToken }),
  
  refresh: (refreshToken: string) =>
    api.post('/api/auth/refresh', { refresh_token: refreshToken }),
};

// Chat API
export const chat = {
  sendMessage: (message: string, conversationId?: number, useRag: boolean = true) =>
    api.post('/api/chat/message', { message, conversation_id: conversationId, use_rag: useRag }),
  
  getConversations: () =>
    api.get('/api/chat/conversations'),
  
  createConversation: (title?: string, userId: number = 1) =>
    api.post('/api/chat/conversations', { title, user_id: userId }),
  
  updateConversation: (conversationId: number, title: string) =>
    api.put(`/api/chat/conversations/${conversationId}`, { title }),
  
  deleteConversation: (conversationId: number) =>
    api.delete(`/api/chat/conversations/${conversationId}`),
  
  getConversationMessages: (conversationId: number) =>
    api.get(`/api/chat/conversations/${conversationId}/messages`),
  
  uploadMaterial: (title: string, content: string, subject?: string) =>
    api.post('/api/chat/materials', { title, content, subject }),
  
  getVoices: () =>
    api.get('/api/chat/voices'),
  
  speak: (text: string, voice?: string) =>
    api.post('/api/tts/generate', { text, voice }),
  
  transcribe: (audioBlob: Blob) => {
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.wav');
    formData.append('language', 'en');
    return api.post('/api/transcribe/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

// Transcription API
export const transcription = {
  upload: (file: File, language: string = 'en') => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language);
    return api.post('/api/transcribe/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  getJobStatus: (jobId: number) =>
    api.get(`/api/transcribe/jobs/${jobId}`),
  
  getResult: (jobId: number) =>
    api.get(`/api/transcribe/results/${jobId}`),
};

// TTS API
export const tts = {
  generate: (text: string, voice?: string) =>
    api.post('/api/tts/generate', { text, voice }),
};

// Notifications API
export const notifications = {
  // Get all notifications with optional filters
  getAll: (params?: { type?: string; read?: boolean; limit?: number; offset?: number }) =>
    api.get('/api/notifications', { params }),
  
  // Mark notification as read
  markRead: (notificationId: number) =>
    api.post('/api/notifications/mark-read', { notification_id: notificationId }),
  
  // Mark all notifications as read
  markAllRead: () =>
    api.post('/api/notifications/mark-all-read'),
  
  // Delete notification
  delete: (notificationId: number) =>
    api.delete(`/api/notifications/${notificationId}`),
  
  // Get unread count
  getUnreadCount: () =>
    api.get('/api/notifications/unread-count'),
  
  // Get notification preferences
  getPreferences: () =>
    api.get('/api/notifications/preferences'),
  
  // Update notification preferences
  updatePreferences: (preferences: {
    email_enabled?: boolean;
    push_enabled?: boolean;
    assignment_notifications?: boolean;
    grade_notifications?: boolean;
    message_notifications?: boolean;
    achievement_notifications?: boolean;
    friend_request_notifications?: boolean;
    study_reminder_notifications?: boolean;
  }) =>
    api.put('/api/notifications/preferences', preferences),
};

// Messages API
export const messages = {
  // Send a message
  send: (recipientId: number, content: string, subject?: string) =>
    api.post('/api/messages/send', { recipient_id: recipientId, content, subject }),
  
  // Get all conversations
  getConversations: () =>
    api.get('/api/messages/conversations'),
  
  // Get conversation with specific user
  getConversation: (userId: number) =>
    api.get(`/api/messages/conversation/${userId}`),
  
  // Mark messages as read
  markRead: (messageIds: number[]) =>
    api.post('/api/messages/mark-read', { message_ids: messageIds }),
  
  // Delete message
  delete: (messageId: number) =>
    api.delete(`/api/messages/${messageId}`),
};

export default api;
