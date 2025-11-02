"""
Redis Client Utilities
Redis connection and operations for caching and job queues
"""
import redis
from typing import Optional, Any
import json
import os


# Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Create Redis client
_redis_client: Optional[redis.Redis] = None


def get_redis_client() -> redis.Redis:
    """
    Get Redis client (singleton pattern)
    
    Returns:
        Redis client instance
    """
    global _redis_client
    
    if _redis_client is None:
        _redis_client = redis.from_url(
            REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_keepalive=True,
            health_check_interval=30
        )
    
    return _redis_client


def cache_set(key: str, value: Any, expire: Optional[int] = None) -> bool:
    """
    Set a value in Redis cache
    
    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        expire: Expiration time in seconds
        
    Returns:
        True if successful
    """
    client = get_redis_client()
    serialized = json.dumps(value)
    
    if expire:
        return client.setex(key, expire, serialized)
    else:
        return client.set(key, serialized)


def cache_get(key: str) -> Optional[Any]:
    """
    Get a value from Redis cache
    
    Args:
        key: Cache key
        
    Returns:
        Cached value or None if not found
    """
    client = get_redis_client()
    value = client.get(key)
    
    if value:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    
    return None


def cache_delete(key: str) -> bool:
    """
    Delete a value from Redis cache
    
    Args:
        key: Cache key
        
    Returns:
        True if key was deleted
    """
    client = get_redis_client()
    return bool(client.delete(key))


def queue_push(queue_name: str, item: Any) -> int:
    """
    Push an item to a Redis queue
    
    Args:
        queue_name: Name of the queue
        item: Item to push (will be JSON serialized)
        
    Returns:
        Length of the queue after push
    """
    client = get_redis_client()
    serialized = json.dumps(item)
    return client.rpush(queue_name, serialized)


def queue_pop(queue_name: str, timeout: int = 0) -> Optional[Any]:
    """
    Pop an item from a Redis queue (blocking)
    
    Args:
        queue_name: Name of the queue
        timeout: Timeout in seconds (0 = block indefinitely)
        
    Returns:
        Popped item or None if timeout
    """
    client = get_redis_client()
    result = client.blpop(queue_name, timeout=timeout)
    
    if result:
        _, value = result
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    
    return None


def queue_length(queue_name: str) -> int:
    """
    Get the length of a Redis queue
    
    Args:
        queue_name: Name of the queue
        
    Returns:
        Queue length
    """
    client = get_redis_client()
    return client.llen(queue_name)
