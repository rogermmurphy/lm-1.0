"""
Session Manager for Authentication Service
Redis-based server-side session management
"""
import uuid
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from lm_common.redis_client import get_redis_client


class SessionManager:
    """Manages user sessions in Redis"""
    
    def __init__(self):
        self.redis = get_redis_client()
        self.session_ttl = 86400  # 24 hours in seconds
        
    def create_session(
        self,
        user_id: int,
        access_token: str,
        refresh_token: str,
        device_info: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new session for a user
        
        Args:
            user_id: User ID
            access_token: JWT access token
            refresh_token: JWT refresh token
            device_info: Optional device information (user_agent, ip_address)
            
        Returns:
            session_id: Unique session identifier
        """
        session_id = str(uuid.uuid4())
        now = datetime.utcnow()
        expires_at = now + timedelta(seconds=self.session_ttl)
        
        session_data = {
            'session_id': session_id,
            'user_id': user_id,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'created_at': now.isoformat(),
            'expires_at': expires_at.isoformat(),
            'last_activity': now.isoformat(),
            'device_info': device_info or {}
        }
        
        # Store session in Redis
        session_key = f'session:{session_id}'
        self.redis.setex(
            session_key,
            self.session_ttl,
            json.dumps(session_data)
        )
        
        # Add to user's session set
        user_sessions_key = f'user:sessions:{user_id}'
        self.redis.sadd(user_sessions_key, session_id)
        self.redis.expire(user_sessions_key, self.session_ttl)
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session data by session ID
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session data dict or None if not found
        """
        session_key = f'session:{session_id}'
        session_data = self.redis.get(session_key)
        
        if not session_data:
            return None
            
        return json.loads(session_data)
    
    def validate_session(self, session_id: str) -> bool:
        """
        Validate that a session exists and is active
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if session is valid, False otherwise
        """
        session_data = self.get_session(session_id)
        
        if not session_data:
            return False
        
        # Check if session has expired
        expires_at = datetime.fromisoformat(session_data['expires_at'])
        if datetime.utcnow() > expires_at:
            self.terminate_session(session_id)
            return False
        
        # Update last activity
        self.update_activity(session_id)
        
        return True
    
    def update_activity(self, session_id: str):
        """Update last activity timestamp for session"""
        session_data = self.get_session(session_id)
        
        if session_data:
            session_data['last_activity'] = datetime.utcnow().isoformat()
            session_key = f'session:{session_id}'
            
            # Update with original TTL
            ttl = self.redis.ttl(session_key)
            if ttl > 0:
                self.redis.setex(session_key, ttl, json.dumps(session_data))
    
    def refresh_session(
        self,
        session_id: str,
        new_access_token: str,
        new_refresh_token: Optional[str] = None
    ) -> bool:
        """
        Refresh session with new tokens
        
        Args:
            session_id: Session identifier
            new_access_token: New JWT access token
            new_refresh_token: Optional new refresh token
            
        Returns:
            True if successful, False if session not found
        """
        session_data = self.get_session(session_id)
        
        if not session_data:
            return False
        
        # Update tokens
        session_data['access_token'] = new_access_token
        if new_refresh_token:
            session_data['refresh_token'] = new_refresh_token
        session_data['last_activity'] = datetime.utcnow().isoformat()
        
        # Store updated session
        session_key = f'session:{session_id}'
        self.redis.setex(
            session_key,
            self.session_ttl,
            json.dumps(session_data)
        )
        
        return True
    
    def terminate_session(self, session_id: str) -> bool:
        """
        Terminate a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if session was terminated, False if not found
        """
        session_data = self.get_session(session_id)
        
        if not session_data:
            return False
        
        user_id = session_data['user_id']
        
        # Remove from Redis
        session_key = f'session:{session_id}'
        self.redis.delete(session_key)
        
        # Remove from user's session set
        user_sessions_key = f'user:sessions:{user_id}'
        self.redis.srem(user_sessions_key, session_id)
        
        return True
    
    def get_user_sessions(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get all active sessions for a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of session data dicts
        """
        user_sessions_key = f'user:sessions:{user_id}'
        session_ids = self.redis.smembers(user_sessions_key)
        
        sessions = []
        for session_id_bytes in session_ids:
            session_id = session_id_bytes.decode('utf-8') if isinstance(session_id_bytes, bytes) else session_id_bytes
            session_data = self.get_session(session_id)
            
            if session_data:
                # Remove sensitive token data for listing
                safe_session = {
                    'session_id': session_data['session_id'],
                    'user_id': session_data['user_id'],
                    'created_at': session_data['created_at'],
                    'expires_at': session_data['expires_at'],
                    'last_activity': session_data['last_activity'],
                    'device_info': session_data.get('device_info', {})
                }
                sessions.append(safe_session)
            else:
                # Clean up stale session reference
                self.redis.srem(user_sessions_key, session_id)
        
        return sessions
    
    def terminate_all_user_sessions(self, user_id: int) -> int:
        """
        Terminate all sessions for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Number of sessions terminated
        """
        user_sessions_key = f'user:sessions:{user_id}'
        session_ids = self.redis.smembers(user_sessions_key)
        
        count = 0
        for session_id_bytes in session_ids:
            session_id = session_id_bytes.decode('utf-8') if isinstance(session_id_bytes, bytes) else session_id_bytes
            if self.terminate_session(session_id):
                count += 1
        
        # Clean up user sessions set
        self.redis.delete(user_sessions_key)
        
        return count
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions (maintenance task)
        
        Returns:
            Number of sessions cleaned up
        """
        # Redis TTL handles automatic expiry, but this method
        # can be used for manual cleanup if needed
        
        # Get all session keys
        session_keys = self.redis.keys('session:*')
        
        count = 0
        for key_bytes in session_keys:
            key = key_bytes.decode('utf-8') if isinstance(key_bytes, bytes) else key_bytes
            session_id = key.split(':')[1]
            
            if not self.validate_session(session_id):
                count += 1
        
        return count


# Singleton instance
_session_manager = None

def get_session_manager() -> SessionManager:
    """Get singleton SessionManager instance"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
