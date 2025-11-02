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
      const token = localStorage.getItem('access_token');
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
        const refreshToken = localStorage.getItem('refresh_token');
        
        if (refreshToken) {
          try {
            const response = await axios.post(`${API_URL}/api/auth/refresh`, {
              refresh_token: refreshToken,
            });
            
            const { access_token } = response.data;
            localStorage.setItem('access_token', access_token);
            
            // Retry original request with new token
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
            return axios(originalRequest);
          } catch (refreshError) {
            // Refresh failed, clear tokens and redirect to login
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
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
  
  uploadMaterial: (title: string, content: string, subject?: string) =>
    api.post('/api/chat/materials', { title, content, subject }),
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

export default api;
