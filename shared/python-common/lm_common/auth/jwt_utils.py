"""
JWT Token Utilities
JWT token generation and validation for microservices
Extracted from POC 12 - Tested and Validated
"""
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os


# Configuration from environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


def create_access_token(
    user_id: int,
    email: str,
    secret_key: str = SECRET_KEY,
    algorithm: str = ALGORITHM,
    expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
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
    secret_key: str = SECRET_KEY,
    algorithm: str = ALGORITHM,
    expires_days: int = REFRESH_TOKEN_EXPIRE_DAYS
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
    secret_key: str = SECRET_KEY,
    algorithm: str = ALGORITHM
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
        return None
    except jwt.InvalidTokenError:
        return None


def verify_access_token(
    token: str,
    secret_key: str = SECRET_KEY,
    algorithm: str = ALGORITHM
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
        return None
    
    try:
        return int(payload.get("sub"))
    except (ValueError, TypeError):
        return None


def verify_refresh_token(
    token: str,
    secret_key: str = SECRET_KEY,
    algorithm: str = ALGORITHM
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
        payload = jwt.decode(token, options={"verify_signature": False})
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            return datetime.fromtimestamp(exp_timestamp)
    except Exception:
        pass
    
    return None
