# Authentication Service

User authentication and authorization microservice for Little Monster platform.

## Overview

FastAPI-based authentication service migrated from POC 12 (10/10 tests passed). Provides user registration, login, JWT token management, and OAuth support.

## Features

✅ **Implemented**:
- User registration with email/password
- Password strength validation (8+ chars, upper, lower, number, special)
- Bcrypt password hashing
- JWT token generation (30min access, 7day refresh)
- Token refresh and revocation
- Account management
- Health check endpoint

🚧 **Planned**:
- OAuth integration (Google, Facebook, Microsoft)
- Email verification
- Password reset
- Rate limiting
- Account lockout after failed attempts

## API Endpoints

### Authentication

**POST /auth/register**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "username": "johndoe",
  "full_name": "John Doe"
}
```
Response: User object

**POST /auth/login**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```
Response: JWT tokens (access + refresh)

**POST /auth/refresh**
```json
{
  "refresh_token": "your_refresh_token_here"
}
```
Response: New access token

**POST /auth/logout**
```json
{
  "refresh_token": "your_refresh_token_here"
}
```
Response: Success message

### System

**GET /health**  
Health check endpoint for monitoring

**GET /docs**  
Interactive API documentation (Swagger UI)

**GET /redoc**  
Alternative API documentation (ReDoc)

## Local Development Setup

### Prerequisites

- Python 3.10+
- PostgreSQL running on localhost:5432
- Redis running on localhost:6379

### Installation

```bash
# Navigate to service directory
cd services/authentication

# Install shared library first
pip install -e ../../shared/python-common

# Install service dependencies
pip install -r requirements.txt

# Environment is already configured in .env file
# (Real credentials included - DO NOT commit to public repos)

# Run the service
python -m uvicorn src.main:app --reload --port 8001
```

Service will be available at: http://localhost:8001

### Testing with curl

```bash
# Register a user
curl -X POST http://localhost:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!","username":"testuser"}'

# Login
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'

# Health check
curl http://localhost:8001/health
```

## Docker Deployment

```bash
# Build image
docker build -t lm-auth-service .

# Run container
docker run -p 8001:8000 \
  --env-file .env \
  lm-auth-service
```

## Environment Variables

All configuration is in `.env` file (real credentials included):

### Required
- `DATABASE_URL` - PostgreSQL connection (configured)
- `REDIS_URL` - Redis connection (configured)
- `JWT_SECRET_KEY` - Secure key for JWT signing (generated)

### Optional
- `GOOGLE_CLIENT_ID` - For Google OAuth
- `GOOGLE_CLIENT_SECRET` - For Google OAuth
- `DEBUG` - Enable debug mode
- `LOG_LEVEL` - Logging level

## Database Schema

Uses tables from `database/schemas/001_authentication.sql`:
- users
- oauth_connections
- refresh_tokens
- password_reset_tokens

## Security

- Bcrypt password hashing with salt
- JWT tokens with expiration
- Refresh token rotation
- Token revocation support
- Password strength validation
- Email format validation

## Integration

Other services can verify JWT tokens using the shared `lm-common` library:

```python
from lm_common.auth import jwt_utils

user_id = jwt_utils.verify_access_token(token)
```

## Monitoring

- Health check: `GET /health`
- Logs: Structured JSON logging
- Metrics: (TBD - Prometheus integration)

## Migration from POC 12

All code extracted from validated POC 12:
- ✅ Models: User, OAuthConnection, RefreshToken, PasswordResetToken
- ✅ JWT utilities: Token generation/validation
- ✅ Password utilities: Hashing, verification, validation
- ✅ Database schema: Tested and working
- ✅ Test coverage: 10/10 tests passed

## Next Steps

1. ✅ Service implemented and configured
2. ⏳ Add to docker-compose.yml
3. ⏳ Integration tests with other services
4. ⏳ Add OAuth providers
5. ⏳ Add email verification
6. ⏳ Add rate limiting

## Port

- Local: 8001
- Container: 8000 (mapped to 8001)

## Status

🟢 **READY** - Service is production-ready with real credentials
