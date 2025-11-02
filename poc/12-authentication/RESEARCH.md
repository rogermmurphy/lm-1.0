# Authentication Research: OAuth2 & Social Login for Little Monster

## Executive Summary

This document analyzes Python authentication libraries for implementing OAuth 2.0 and social login (Google, Facebook, Microsoft, etc.) plus direct email/password registration for the Little Monster educational platform.

**Recommendation**: Use **Authlib** with **FastAPI** for OAuth2, combined with **Passlib** for password hashing and **PyJWT** for token management.

---

## Research Findings

### Top Python OAuth2 Libraries

#### 1. Authlib ⭐ (RECOMMENDED)
**Repository**: https://github.com/lepture/authlib
**Documentation**: https://docs.authlib.org/

**Pros**:
- Most comprehensive and modern OAuth 2.0/OpenID Connect library
- Supports all major OAuth 2.0 grants (Authorization Code, Implicit, Password, Client Credentials, Refresh Token)
- Built-in support for Flask and FastAPI integration
- Handles JWT, JWS, JWE, JWK natively
- Active maintenance (last update: 2024)
- Excellent documentation with examples
- Supports asymmetric cryptography for token signing
- Built-in token introspection
- PKCE (Proof Key for Code Exchange) support for enhanced security

**Cons**:
- Slightly steeper learning curve due to comprehensive features
- Requires manual OAuth provider configuration

**Key Features**:
- OAuth 2.0 Client (for consuming OAuth APIs)
- OAuth 2.0 Server (for providing OAuth APIs)
- OpenID Connect support
- JWT/JWS/JWE/JWK support
- Integration with SQLAlchemy for token storage

**Code Example**:
```python
from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749 import grants

# Setup Authorization Server
authorization = AuthorizationServer(app, query_client=query_client, save_token=save_token)

# Register Password Grant
class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    def authenticate_user(self, username, password):
        # Your user authentication logic
        return user

authorization.register_grant(PasswordGrant)
```

#### 2. OAuthLib
**Repository**: https://github.com/oauthlib/oauthlib
**Documentation**: https://oauthlib.readthedocs.io/

**Pros**:
- Core OAuth 1.0a and OAuth 2.0 implementation
- Used as foundation for many other libraries
- Strict RFC compliance
- Mature and battle-tested

**Cons**:
- Lower-level API (requires more boilerplate)
- Less integrated with web frameworks
- Requires wrapper libraries like Requests-OAuthlib

**Use Case**: Good as a foundation library but not ideal for direct use in applications.

#### 3. Python Social Auth
**Repository**: https://github.com/python-social-auth/social-core
**Documentation**: https://python-social-auth.readthedocs.io/

**Pros**:
- Pre-built OAuth configurations for 50+ providers
- Less code to write for standard OAuth flows
- Multiple framework support (Flask, Django, Pyramid)
- Batteries-included approach

**Cons**:
- Less active development than Authlib
- Can be opaque when things go wrong
- Less flexible for custom OAuth implementations
- Heavier dependency footprint

**Use Case**: Good for rapid prototyping with many providers, but less control.

#### 4. FastAPI-Users
**Repository**: https://github.com/fastapi-users/fastapi-users
**Documentation**: https://fastapi-users.github.io/

**Pros**:
- Specifically designed for FastAPI
- Complete user management solution (registration, login, password reset)
- Built-in OAuth2 support
- JWT and cookie-based authentication
- SQLAlchemy and MongoDB support

**Cons**:
- Tightly coupled to FastAPI
- Opinionated architecture
- Less flexibility for custom workflows

**Use Case**: Excellent for FastAPI projects wanting a complete solution.

---

## OAuth2 Provider Setup

### Google OAuth2
**Documentation**: https://developers.google.com/identity/protocols/oauth2

**Setup Steps**:
1. Create project in Google Cloud Console
2. Enable Google+ API
3. Create OAuth 2.0 credentials (Web application)
4. Configure authorized redirect URIs
5. Obtain Client ID and Client Secret

**Scopes Required**:
- `openid` - OpenID Connect authentication
- `email` - User's email address
- `profile` - Basic profile information

**Authlib Configuration**:
```python
GOOGLE_CLIENT_ID = 'your-client-id.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'your-client-secret'
GOOGLE_AUTHORIZE_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_ACCESS_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_API_BASE_URL = 'https://www.googleapis.com/oauth2/v2/'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'
```

### Facebook OAuth2
**Documentation**: https://developers.facebook.com/docs/facebook-login

**Setup Steps**:
1. Create app in Facebook Developers
2. Add Facebook Login product
3. Configure valid OAuth redirect URIs
4. Obtain App ID and App Secret
5. Submit for app review (for production)

**Scopes Required**:
- `email` - User's email address
- `public_profile` - Basic profile information

**Authlib Configuration**:
```python
FACEBOOK_CLIENT_ID = 'your-app-id'
FACEBOOK_CLIENT_SECRET = 'your-app-secret'
FACEBOOK_AUTHORIZE_URL = 'https://www.facebook.com/v18.0/dialog/oauth'
FACEBOOK_ACCESS_TOKEN_URL = 'https://graph.facebook.com/v18.0/oauth/access_token'
FACEBOOK_API_BASE_URL = 'https://graph.facebook.com/v18.0/'
```

### Microsoft OAuth2 (Azure AD)
**Documentation**: https://learn.microsoft.com/en-us/azure/active-directory/develop/

**Setup Steps**:
1. Register application in Azure Portal
2. Create client secret
3. Configure redirect URIs
4. Set API permissions

**Scopes Required**:
- `openid` - OpenID Connect
- `email` - User's email
- `profile` - Profile information

**Authlib Configuration**:
```python
MICROSOFT_CLIENT_ID = 'your-application-id'
MICROSOFT_CLIENT_SECRET = 'your-client-secret'
MICROSOFT_AUTHORIZE_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
MICROSOFT_ACCESS_TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
```

---

## Security Best Practices

### Password Hashing
**Library**: Passlib with bcrypt backend
**Why**: Industry standard, configurable work factor, salt built-in

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash("user_password")

# Verify password
is_valid = pwd_context.verify("user_password", hashed)
```

### JWT Token Management
**Library**: PyJWT
**Token Types**:
- **Access Token**: Short-lived (15-30 minutes), used for API access
- **Refresh Token**: Long-lived (7-30 days), used to obtain new access tokens

```python
import jwt
from datetime import datetime, timedelta

# Generate access token
access_token = jwt.encode(
    {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "type": "access"
    },
    SECRET_KEY,
    algorithm="HS256"
)

# Generate refresh token
refresh_token = jwt.encode(
    {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=7),
        "type": "refresh"
    },
    SECRET_KEY,
    algorithm="HS256"
)
```

### Session Management with Redis
**Why Redis**:
- Fast in-memory storage
- Built-in TTL (Time To Live) for automatic expiration
- Already part of Little Monster infrastructure

```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Store session
session_data = {
    "user_id": user_id,
    "email": user_email,
    "login_time": datetime.utcnow().isoformat()
}
redis_client.setex(
    f"session:{session_id}",
    3600,  # 1 hour expiration
    json.dumps(session_data)
)

# Retrieve session
session = redis_client.get(f"session:{session_id}")
if session:
    session_data = json.loads(session)
```

### CSRF Protection
**Strategy**: Use double-submit cookie pattern or synchronizer token

```python
import secrets

# Generate CSRF token
csrf_token = secrets.token_urlsafe(32)

# Store in session and require in form submissions
```

### Rate Limiting
**Strategy**: Use Redis for distributed rate limiting

```python
def check_rate_limit(user_id, action, max_attempts, window_seconds):
    key = f"rate_limit:{user_id}:{action}"
    current = redis_client.get(key)
    
    if current and int(current) >= max_attempts:
        return False
    
    pipe = redis_client.pipeline()
    pipe.incr(key)
    pipe.expire(key, window_seconds)
    pipe.execute()
    
    return True
```

---

## Database Schema Design

### users table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),  -- NULL for OAuth-only users
    full_name VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    
    -- Indexes
    INDEX idx_email (email),
    INDEX idx_username (username)
);
```

### oauth_connections table
```sql
CREATE TABLE oauth_connections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,  -- 'google', 'facebook', 'microsoft'
    provider_user_id VARCHAR(255) NOT NULL,  -- OAuth provider's user ID
    provider_email VARCHAR(255),
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Prevent duplicate OAuth connections
    UNIQUE(provider, provider_user_id),
    
    -- Indexes
    INDEX idx_user_id (user_id),
    INDEX idx_provider_user (provider, provider_user_id)
);
```

### refresh_tokens table (for direct auth)
```sql
CREATE TABLE refresh_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked BOOLEAN DEFAULT FALSE,
    
    -- Indexes
    INDEX idx_token_hash (token_hash),
    INDEX idx_user_id (user_id),
    INDEX idx_expires_at (expires_at)
);
```

### password_reset_tokens table
```sql
CREATE TABLE password_reset_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    used BOOLEAN DEFAULT FALSE,
    
    -- Indexes
    INDEX idx_token_hash (token_hash),
    INDEX idx_expires_at (expires_at)
);
```

---

## Authentication Flow Diagrams

### Direct Registration Flow
```
1. User submits email + password
2. Validate email format and password strength
3. Check if email already exists
4. Hash password with bcrypt
5. Create user record in database
6. Generate email verification token
7. Send verification email
8. Return success response
```

### Direct Login Flow
```
1. User submits email + password
2. Fetch user from database by email
3. Verify password against stored hash
4. Check if user is active and verified
5. Generate access token (JWT, 30 min expiry)
6. Generate refresh token (JWT, 7 day expiry)
7. Store refresh token in database
8. Update last_login timestamp
9. Return tokens to client
```

### OAuth2 Flow (Google/Facebook/Microsoft)
```
1. User clicks "Login with Google"
2. Redirect to OAuth provider authorization URL
3. User authenticates with provider
4. Provider redirects back with authorization code
5. Exchange code for access token
6. Fetch user profile from provider API
7. Check if OAuth connection exists in database
   - If yes: Get existing user
   - If no: Create new user and OAuth connection
8. Generate application access/refresh tokens
9. Update last_login timestamp
10. Return tokens to client
```

### Token Refresh Flow
```
1. Client sends expired access token + refresh token
2. Verify refresh token signature and expiration
3. Check if refresh token exists in database and not revoked
4. Generate new access token
5. Optionally rotate refresh token
6. Return new tokens to client
```

---

## Implementation Architecture

### Recommended Stack
- **Web Framework**: FastAPI (async, modern, excellent docs)
- **OAuth2 Library**: Authlib (comprehensive, well-maintained)
- **Password Hashing**: Passlib with bcrypt
- **JWT Library**: PyJWT
- **Session Store**: Redis (existing infrastructure)
- **Database**: PostgreSQL (existing infrastructure)
- **ORM**: SQLAlchemy (matches POC 08 & 09 patterns)

### Project Structure
```
poc/12-authentication/
├── README.md                    # Overview and setup
├── RESEARCH.md                  # This file
├── START-HERE.md               # Quick start guide
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── schema.sql                 # Database schema
├── config.py                  # Configuration management
├── models.py                  # Database models (SQLAlchemy)
├── auth_service.py            # Main authentication service
├── oauth_providers.py         # OAuth provider configurations
├── password_utils.py          # Password hashing utilities
├── jwt_utils.py              # JWT token utilities
├── session_manager.py        # Redis session management
├── email_service.py          # Email verification service
├── test_auth.py              # Authentication tests
└── main.py                   # FastAPI application
```

### Key Dependencies
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
authlib==1.2.1
passlib[bcrypt]==1.7.4
pyjwt==2.8.0
python-multipart==0.0.6
email-validator==2.1.0
redis==5.0.1
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

---

## Security Considerations

### 1. Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character
- Not in common password list

### 2. Token Security
- Use HTTPS only in production
- Store tokens securely on client (httpOnly cookies or secure storage)
- Implement token rotation
- Short access token lifespan (15-30 minutes)
- Longer refresh token lifespan (7-30 days)
- Revoke tokens on logout

### 3. OAuth2 Security
- Validate redirect URIs strictly
- Use state parameter to prevent CSRF
- Implement PKCE for public clients
- Verify token signatures
- Validate token expiration

### 4. Rate Limiting
- Login attempts: 5 per minute per IP
- Registration: 3 per hour per IP
- Password reset: 3 per hour per email
- OAuth callback: 10 per minute per IP

### 5. Email Verification
- Required for direct registration
- Token expires in 24 hours
- One-time use only
- Rate limit resend requests

---

## Comparison Matrix

| Feature | Authlib | OAuthLib | Python Social Auth | FastAPI-Users |
|---------|---------|----------|-------------------|---------------|
| OAuth 2.0 Client | ✅ | ✅ | ✅ | ✅ |
| OAuth 2.0 Server | ✅ | ✅ | ❌ | ✅ |
| OpenID Connect | ✅ | Partial | ✅ | ✅ |
| Framework Integration | Flask, FastAPI | Manual | Multiple | FastAPI only |
| Pre-built Providers | Manual config | Manual | 50+ providers | Google, GitHub, etc. |
| Active Development | ✅ Very Active | ✅ Active | ⚠️ Moderate | ✅ Active |
| Documentation | Excellent | Good | Good | Excellent |
| Learning Curve | Moderate | High | Low | Low |
| Flexibility | High | High | Moderate | Low |
| Production Ready | ✅ | ✅ | ✅ | ✅ |

---

## Conclusion

**Recommended Approach**: Use **Authlib** with **FastAPI** for implementing OAuth2 authentication with social login providers (Google, Facebook, Microsoft) and direct email/password registration.

**Rationale**:
1. **Authlib** provides comprehensive OAuth 2.0/OpenID Connect support
2. **FastAPI** offers modern, async Python with excellent documentation
3. Integrates well with existing PostgreSQL and Redis infrastructure
4. Provides flexibility for custom authentication flows
5. Active development and community support
6. Production-ready with proper security implementations

**Next Steps**:
1. Set up OAuth provider credentials (Google, Facebook, Microsoft)
2. Implement database schema
3. Create authentication service with Authlib
4. Implement direct registration with Passlib
5. Set up JWT token management
6. Integrate Redis session management
7. Test all authentication flows
8. Document API endpoints

---

## References

- [Authlib Documentation](https://docs.authlib.org/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [OAuth 2.0 RFC 6749](https://tools.ietf.org/html/rfc6749)
- [OpenID Connect Specification](https://openid.net/specs/openid-connect-core-1_0.html)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [Google OAuth2 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Facebook Login Documentation](https://developers.facebook.com/docs/facebook-login)
- [Microsoft Identity Platform](https://learn.microsoft.com/en-us/azure/active-directory/develop/)
