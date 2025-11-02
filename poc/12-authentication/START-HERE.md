# START HERE: POC 12 Authentication & User Management

## Overview

POC 12 implements multi-provider OAuth2/SSO authentication (Google, Facebook, Microsoft) and direct email/password registration for the Little Monster educational platform.

**Status**: RESEARCH PHASE COMPLETE  
**Recommendation**: Authlib + FastAPI + Passlib + PyJWT  
**Next Phase**: Implementation

---

## Quick Start

### Prerequisites

1. **PostgreSQL Database** (Running on port 5432)
   - Container: `lm-postgres`
   - Database: `lm_db`
   - User: `lmuser`

2. **Redis** (Running on port 6379)
   - Container: `lm-redis`
   - Used for session management

3. **Python 3.11+**

### Setup Steps

#### 1. Install Dependencies

```bash
cd poc/12-authentication
pip install -r requirements.txt
```

#### 2. Configure Environment Variables

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env with your actual credentials
# At minimum, update these:
# - SECRET_KEY (generate a random string)
# - JWT_SECRET_KEY (generate another random string)
# - DATABASE_URL (if different from default)
# - REDIS_URL (if different from default)
```

**Generate Secret Keys** (Python):
```python
import secrets
print(secrets.token_urlsafe(32))  # Run twice for two different keys
```

#### 3. Set Up Database Schema

```bash
# Make sure PostgreSQL is running
docker ps | grep lm-postgres

# Apply the schema
psql -h localhost -p 5432 -U lmuser -d lm_db -f schema.sql
```

#### 4. Set Up OAuth Providers (Optional for Testing)

**Google OAuth2:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials (Web application)
5. Add authorized redirect URI: `http://localhost:8000/auth/callback/google`
6. Copy Client ID and Client Secret to `.env`

**Facebook OAuth2:**
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add Facebook Login product
4. Add redirect URI: `http://localhost:8000/auth/callback/facebook`
5. Copy App ID and App Secret to `.env`

**Microsoft OAuth2:**
1. Go to [Azure Portal](https://portal.azure.com/)
2. Register a new application
3. Create a client secret
4. Add redirect URI: `http://localhost:8000/auth/callback/microsoft`
5. Copy Application ID and Client Secret to `.env`

---

## What's Included

### Research & Documentation
- ✅ **RESEARCH.md** - Comprehensive analysis of authentication libraries
- ✅ **README.md** - Project overview and requirements
- ✅ **Database Schema** - Complete PostgreSQL schema with indexes
- ✅ **Environment Config** - Template for all required variables

### Implementation (Future Steps)
- ⏳ Authentication service with Authlib
- ⏳ Direct registration/login endpoints
- ⏳ OAuth2 provider integrations
- ⏳ JWT token management
- ⏳ Redis session management
- ⏳ Password reset functionality
- ⏳ Email verification
- ⏳ Rate limiting
- ⏳ API documentation
- ⏳ Test suite

---

## Key Findings from Research

### Recommended Technology Stack

1. **Authlib** - OAuth2/OpenID Connect library
   - Most comprehensive and modern
   - Excellent FastAPI integration
   - Active maintenance (2024)
   - Production-ready

2. **FastAPI** - Web framework
   - Async support
   - Built-in security features
   - Automatic API documentation
   - Great developer experience

3. **Passlib + bcrypt** - Password hashing
   - Industry standard
   - Configurable work factor
   - Built-in salt handling

4. **PyJWT** - Token management
   - JWT creation and validation
   - Multiple algorithms support
   - Simple API

5. **Redis** - Session storage
   - Fast in-memory storage
   - Built-in TTL expiration
   - Already in infrastructure

### Security Features

✅ **Password Security:**
- Bcrypt hashing with salt
- Minimum 8 characters
- Uppercase, lowercase, number, special char required
- Common password blacklist

✅ **Token Security:**
- Short-lived access tokens (30 minutes)
- Long-lived refresh tokens (7 days)
- Token rotation on refresh
- Database-backed revocation

✅ **OAuth2 Security:**
- State parameter for CSRF protection
- PKCE support for enhanced security
- Strict redirect URI validation
- Token signature verification

✅ **Rate Limiting:**
- Login: 5 attempts per minute
- Registration: 3 attempts per hour
- Password reset: 3 attempts per hour
- OAuth callback: 10 per minute

---

## Database Schema Overview

### Tables Created

1. **users** - User accounts
   - Email/username (unique)
   - Password hash (NULL for OAuth-only)
   - Verification status
   - Active status

2. **oauth_connections** - OAuth provider links
   - Links users to Google/Facebook/Microsoft accounts
   - Stores provider user IDs
   - Caches OAuth tokens

3. **refresh_tokens** - JWT refresh tokens
   - Token hashes (for validation)
   - Expiration tracking
   - Revocation support

4. **password_reset_tokens** - Password reset
   - One-time use tokens
   - 24-hour expiration
   - Usage tracking

---

## Authentication Flows

### Direct Registration
```
1. User submits email + password
2. Validate email format and password strength
3. Check email availability
4. Hash password with bcrypt
5. Create user record
6. Generate verification token
7. Send verification email
8. Return success response
```

### Direct Login
```
1. User submits email + password
2. Fetch user from database
3. Verify password hash
4. Check user is active and verified
5. Generate access token (30 min)
6. Generate refresh token (7 days)
7. Store refresh token in database
8. Return tokens to client
```

### OAuth2 Login (Google/Facebook/Microsoft)
```
1. User clicks "Login with Provider"
2. Redirect to provider authorization page
3. User authenticates with provider
4. Provider redirects with authorization code
5. Exchange code for access token
6. Fetch user profile from provider
7. Check if connection exists
   - Yes: Login existing user
   - No: Create new user + connection
8. Generate application tokens
9. Return tokens to client
```

### Token Refresh
```
1. Client sends expired access token + refresh token
2. Verify refresh token signature
3. Check token not revoked in database
4. Generate new access token
5. Optionally rotate refresh token
6. Return new tokens
```

---

## Next Steps for Implementation

### Phase 1: Core Authentication (Week 1)
1. Create FastAPI application structure
2. Implement database models with SQLAlchemy
3. Create password utilities (hashing, validation)
4. Implement JWT token utilities
5. Build direct registration endpoint
6. Build direct login endpoint
7. Implement token refresh endpoint

### Phase 2: OAuth Integration (Week 2)
1. Configure Authlib OAuth clients
2. Implement Google OAuth flow
3. Implement Facebook OAuth flow
4. Implement Microsoft OAuth flow
5. Handle OAuth callbacks
6. Link OAuth accounts to existing users

### Phase 3: Additional Features (Week 3)
1. Email verification system
2. Password reset flow
3. Session management with Redis
4. Rate limiting implementation
5. CSRF protection
6. API documentation

### Phase 4: Testing & Documentation (Week 4)
1. Unit tests for all endpoints
2. Integration tests for OAuth flows
3. Security testing
4. Performance testing
5. API documentation
6. Deployment guide

---

## Testing OAuth Without Real Providers

For development/testing without setting up real OAuth providers:

1. **Use Mock OAuth Server**
   - Create test endpoints that simulate OAuth flow
   - Useful for CI/CD pipelines

2. **Test Direct Authentication First**
   - Email/password registration works without OAuth setup
   - Verify core authentication logic

3. **Use Development OAuth Apps**
   - Create test apps on each provider
   - Use localhost redirect URIs for testing

---

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker ps | grep lm-postgres

# Test connection
psql -h localhost -p 5432 -U lmuser -d lm_db -c "SELECT version();"
```

### Redis Connection Issues
```bash
# Check if Redis is running
docker ps | grep lm-redis

# Test connection
redis-cli -h localhost -p 6379 ping
```

### OAuth Redirect URI Mismatch
- Ensure redirect URIs in OAuth provider console exactly match those in `.env`
- Must include protocol (http:// or https://)
- Must match port number
- No trailing slashes

### Secret Key Generation
```python
# Generate strong random keys
import secrets
secret_key = secrets.token_urlsafe(32)
jwt_key = secrets.token_urlsafe(32)
print(f"SECRET_KEY={secret_key}")
print(f"JWT_SECRET_KEY={jwt_key}")
```

---

## Resources

### Documentation
- [Authlib Docs](https://docs.authlib.org/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [OAuth 2.0 RFC](https://tools.ietf.org/html/rfc6749)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

### OAuth Provider Docs
- [Google OAuth2](https://developers.google.com/identity/protocols/oauth2)
- [Facebook Login](https://developers.facebook.com/docs/facebook-login)
- [Microsoft Identity](https://learn.microsoft.com/en-us/azure/active-directory/develop/)

### Security Resources
- [OWASP Auth Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

---

## Contact & Support

For questions or issues with POC 12:
1. Review RESEARCH.md for detailed analysis
2. Check README.md for requirements
3. Consult schema.sql for database structure
4. Reference .env.example for configuration

**Research Status**: ✅ COMPLETE  
**Implementation Status**: ⏳ PENDING  
**Testing Status**: ⏳ PENDING
