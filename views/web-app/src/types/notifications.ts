/**
 * TypeScript interfaces for Notifications and Messages
 */

export interface Notification {
  id: number;
  user_id: number;
  type: string;
  title: string;
  message: string;
  data?: Record<string, any>;
  read: boolean;
  created_at: string;
}

export interface NotificationPreferences {
  user_id: number;
  email_enabled: boolean;
  push_enabled: boolean;
  assignment_notifications: boolean;
  grade_notifications: boolean;
  message_notifications: boolean;
  achievement_notifications: boolean;
  friend_request_notifications: boolean;
  study_reminder_notifications: boolean;
  updated_at: string;
}

export interface DirectMessage {
  id: number;
  sender_id: number;
  recipient_id: number;
  subject?: string;
  content: string;
  read: boolean;
  created_at: string;
  sender_username?: string;
  recipient_username?: string;
}

export interface Conversation {
  user_id: number;
  username: string;
  last_message: string;
  last_message_time: string;
  unread_count: number;
}
