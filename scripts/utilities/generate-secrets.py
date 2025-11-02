#!/usr/bin/env python3
"""
Generate secure secrets for environment variables
"""
import secrets
import base64

def generate_jwt_secret():
    """Generate a secure JWT secret key"""
    # Generate 64 bytes of random data
    random_bytes = secrets.token_bytes(64)
    # Base64 encode for easy storage
    return base64.b64encode(random_bytes).decode('utf-8')

if __name__ == "__main__":
    print("JWT_SECRET_KEY=" + generate_jwt_secret())
