"""
POC 12: JWT Token Utilities
JWT token generation and validation
"""
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Default configuration (can be overridden)
DEFAULT_SECRET_KEY = "dev-secret-key-change-in-production"
DEFAULT_ALGORITHM = "HS256"
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
DEFAULT_REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(
    user_id: int,
    email: str,
    secret_key: str = DEFAULT_SECRET_KEY,
    algorithm: str = DEFAULT_ALGORITHM,
    expires_minutes: int = DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    """
    Create a JWT access token
    
    Args:
        user_id: User's database ID
        email: User's email
        secret_key: Secret key for signing
        algorithm: JWT algorithm
        expires_minutes: Token expiration time in minutes
        
    Returns:
        Encoded JWT token string
    """
    expires_at = datetime.utcnow() + timedelta(minutes=expires_minutes)
    
    payload = {
        "sub": str(user_id),
        "email": email,
        "type": "access",
        "exp": expires_at,
        "iat": datetime.utcnow()
    }
    
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def create_refresh_token(
    user_id: int,
    secret_key: str = DEFAULT_SECRET_KEY,
    algorithm: str = DEFAULT_ALGORITHM,
    expires_days: int = DEFAULT_REFRESH_TOKEN_EXPIRE_DAYS
) -> str:
    """
    Create a JWT refresh token
    
    Args:
        user_id: User's database ID
        secret_key: Secret key for signing
        algorithm: JWT algorithm
        expires_days: Token expiration time in days
        
    Returns:
        Encoded JWT token string
    """
    expires_at = datetime.utcnow() + timedelta(days=expires_days)
    
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expires_at,
        "iat": datetime.utcnow()
    }
    
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_token(
    token: str,
    secret_key: str = DEFAULT_SECRET_KEY,
    algorithm: str = DEFAULT_ALGORITHM
) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT token
    
    Args:
        token: JWT token string
        secret_key: Secret key for validation
        algorithm: JWT algorithm
        
    Returns:
        Decoded payload dict or None if invalid
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None


def verify_access_token(
    token: str,
    secret_key: str = DEFAULT_SECRET_KEY,
    algorithm: str = DEFAULT_ALGORITHM
) -> Optional[int]:
    """
    Verify an access token and return user ID
    
    Args:
        token: JWT access token
        secret_key: Secret key for validation
        algorithm: JWT algorithm
        
    Returns:
        User ID if valid, None otherwise
    """
    payload = decode_token(token, secret_key, algorithm)
    
    if not payload:
        return None
    
    if payload.get("type") != "access":
        print("Token is not an access token")
        return None
    
    try:
        return int(payload.get("sub"))
    except (ValueError, TypeError):
        return None


def verify_refresh_token(
    token: str,
    secret_key: str = DEFAULT_SECRET_KEY,
    algorithm: str = DEFAULT_ALGORITHM
) -> Optional[int]:
    """
    Verify a refresh token and return user ID
    
    Args:
        token: JWT refresh token
        secret_key: Secret key for validation
        algorithm: JWT algorithm
        
    Returns:
        User ID if valid, None otherwise
    """
    payload = decode_token(token, secret_key, algorithm)
    
    if not payload:
        return None
    
    if payload.get("type") != "refresh":
        print("Token is not a refresh token")
        return None
    
    try:
        return int(payload.get("sub"))
    except (ValueError, TypeError):
        return None


def get_token_expiration(token: str) -> Optional[datetime]:
    """
    Get the expiration time of a token without validating signature
    
    Args:
        token: JWT token
        
    Returns:
        Expiration datetime or None if invalid
    """
    try:
        # Decode without verification
        payload = jwt.decode(token, options={"verify_signature": False})
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            return datetime.fromtimestamp(exp_timestamp)
    except Exception as e:
        print(f"Error getting token expiration: {e}")
    
    return None
