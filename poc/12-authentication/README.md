# POC 12: Authentication & User Management

## Objective
Implement multi-provider OAuth/SSO authentication (Google, Facebook, etc.) plus direct email/password registration for Little Monster application.

## Requirements

### OAuth/SSO Providers
- Google Sign-In
- Facebook Login
- Microsoft Account
- GitHub (optional)
- Apple Sign-In (optional)

### Direct Registration
- Email + password registration
- Password hashing (bcrypt/argon2)
- Email validation
- Username/email uniqueness

### Security Features
- JWT or session-based authentication
- CSRF protection
- Rate limiting on auth endpoints
- Secure credential storage
- Password reset functionality
- Account verification (email)

## Technology Stack

### Backend
- Python 3.11+
- Flask or FastAPI
- PostgreSQL (existing infrastructure)
- Redis (existing infrastructure for sessions)

### Libraries Under Consideration
1. **Authlib** - Modern OAuth/OIDC library
2. **Python Social Auth** - Multi-provider authentication
3. **Flask-Login** / **FastAPI-Users** - Session management
4. **Passlib** - Password hashing
5. **PyJWT** - JWT token handling
6. **Supabase Auth** - Managed authentication service

## Database Schema (Proposed)

### users table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),  -- NULL for OAuth-only users
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### oauth_connections table
```sql
CREATE TABLE oauth_connections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,  -- 'google', 'facebook', 'microsoft', etc.
    provider_user_id VARCHAR(255) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(provider, provider_user_id)
);
```

### sessions table (Redis or PostgreSQL)
```sql
CREATE TABLE sessions (
    id VARCHAR(255) PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    data TEXT,  -- JSON session data
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Implementation Phases

### Phase 1: Research & Design (Current)
- [x] Create POC directory structure
- [ ] Research authentication libraries
- [ ] Compare OAuth implementation approaches
- [ ] Design complete database schema
- [ ] Design authentication flow
- [ ] Choose implementation approach
- [ ] Document security best practices

### Phase 2: Database Setup
- [ ] Create database tables
- [ ] Set up migrations
- [ ] Test database connectivity
- [ ] Create test data

### Phase 3: Direct Registration
- [ ] Implement email/password registration
- [ ] Password hashing with bcrypt
- [ ] Email validation
- [ ] Login endpoint
- [ ] Session management
- [ ] Password reset flow

### Phase 4: OAuth Integration
- [ ] Set up OAuth provider credentials
- [ ] Implement Google OAuth
- [ ] Implement Facebook OAuth
- [ ] Implement Microsoft OAuth (optional)
- [ ] Handle OAuth callbacks
- [ ] Link OAuth accounts to users

### Phase 5: Testing & Documentation
- [ ] Test direct registration flow
- [ ] Test OAuth flows (all providers)
- [ ] Test account linking
- [ ] Security testing
- [ ] Performance testing
- [ ] Documentation

## Files Structure
```
poc/12-authentication/
├── README.md                    # This file
├── START-HERE.md               # Quick start guide
├── RESEARCH.md                 # Authentication library research
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── schema.sql                 # Database schema
├── auth_service.py            # Main authentication service
├── oauth_providers.py         # OAuth provider configurations
├── password_utils.py          # Password hashing utilities
├── session_manager.py         # Session management
├── test_auth.py              # Authentication tests
└── config.py                 # Configuration management
```

## Environment Variables Required
```
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/lm_db

# Redis
REDIS_URL=redis://localhost:6379/0

# OAuth Providers
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx
FACEBOOK_CLIENT_ID=xxx
FACEBOOK_CLIENT_SECRET=xxx
MICROSOFT_CLIENT_ID=xxx
MICROSOFT_CLIENT_SECRET=xxx

# Security
SECRET_KEY=random-secret-key-here
JWT_SECRET_KEY=another-random-key
SESSION_LIFETIME=3600  # seconds

# Application
APP_URL=http://localhost:5000
OAUTH_CALLBACK_URL=http://localhost:5000/auth/callback
```

## Next Steps
1. Start with authentication library research
2. Create detailed comparison document
3. Choose implementation approach
4. Set up database schema
5. Implement POC with at least 2 OAuth providers

## References
- [Authlib Documentation](https://docs.authlib.org/)
- [Python Social Auth](https://python-social-auth.readthedocs.io/)
- [Flask-Login](https://flask-login.readthedocs.io/)
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/)
- [OAuth 2.0 RFC](https://oauth.net/2/)
- [OpenID Connect](https://openid.net/connect/)
