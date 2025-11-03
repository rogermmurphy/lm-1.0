// Chat-related TypeScript types

export interface Conversation {
  id: number;
  title: string | null;
  message_count: number;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: number;
  conversation_id: number;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
}

export interface ChatMessageRequest {
  conversation_id?: number;
  message: string;
  use_rag?: boolean;
}

export interface ChatMessageResponse {
  conversation_id: number;
  message_id: number;
  response: string;
  sources?: string[];
  created_at: string;
}

export interface ConversationCreateRequest {
  title?: string;
  user_id: number;
}

export interface ConversationUpdateRequest {
  title: string;
}
