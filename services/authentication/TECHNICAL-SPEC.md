# Authentication Service - Technical Specification

## Document Control
- **Version**: 1.0
- **Date**: 2025-11-01
- **Status**: Implementation Complete
- **Service**: Authentication Service

---

## 1. Architecture

### 1.1 Technology Stack

**Framework**: FastAPI 0.104.1
- Async/await support
- Automatic OpenAPI documentation
- Pydantic validation
- Dependency injection

**Database**: PostgreSQL via SQLAlchemy 2.0.23
- ORM models for type safety
- Connection pooling (10 connections, 20 overflow)
- Migration support via Alembic

**Cache/Queue**: Redis 5.0.1
- Session storage
- Token blacklisting
- Future: Rate limiting

**Authentication**: 
- PyJWT 2.8.0 for token generation
- bcrypt 4.1.0 for password hashing
- python-jose for cryptographic operations

### 1.2 Service Architecture

```
┌─────────────────────────────────────────┐
│      Authentication Service             │
│                                         │
│  ┌─────────────┐    ┌───────────────┐ │
│  │   FastAPI   │    │   Routes      │ │
│  │   App       │───▶│  /auth/*      │ │
│  └─────────────┘    └───────────────┘ │
│         │                  │           │
│         ▼                  ▼           │
│  ┌─────────────┐    ┌───────────────┐ │
│  │  Models     │    │   Schemas     │ │
│  │ (SQLAlchemy)│    │  (Pydantic)   │ │
│  └─────────────┘    └───────────────┘ │
│         │                              │
│         ▼                              │
│  ┌─────────────────────────────────┐  │
│  │      lm-common Library          │  │
│  │  • JWT Utils                    │  │
│  │  • Password Utils               │  │
│  │  • Database Connection          │  │
│  │  • Redis Client                 │  │
│  └─────────────────────────────────┘  │
└─────────────────────────────────────────┘
           │              │
           ▼              ▼
    ┌───────────┐  ┌──────────┐
    │PostgreSQL │  │  Redis   │
    └───────────┘  └──────────┘
```

## 2. Data Layer

### 2.1 Database Models

**User Model** (`models.py`):
```python
class User(Base):
    __tablename__ = 'users'
    id: int (PK)
    email: str (unique, indexed)
    username: str (unique, indexed, nullable)
    password_hash: str (nullable for OAuth)
    full_name: str (nullable)
    is_verified: bool (default False)
    is_active: bool (default True, indexed)
    created_at: datetime
    updated_at: datetime (auto-update trigger)
    last_login: datetime (nullable)
```

**RefreshToken Model** (`models.py`):
```python
class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    id: int (PK)
    user_id: int (FK -> users.id)
    token_hash: str (SHA256, unique, indexed)
    expires_at: datetime (indexed)
    created_at: datetime
    revoked: bool (default False, indexed)
    revoked_at: datetime (nullable)
```

### 2.2 Database Indexes

Performance-critical indexes:
- `users.email` - Login lookups
- `users.username` - Profile lookups
- `users.is_active` - Active user queries
- `refresh_tokens.token_hash` - Token verification
- `refresh_tokens.user_id` - User token lookups
- `refresh_tokens.revoked` - Active token queries

## 3. API Layer

### 3.1 Request Schemas (Pydantic)

**UserRegisterRequest**:
```python
email: EmailStr (validated)
password: str (min_length=8)
username: Optional[str] (max_length=100)
full_name: Optional[str] (max_length=255)
```

**UserLoginRequest**:
```python
email: EmailStr
password: str
```

**TokenRefreshRequest**:
```python
refresh_token: str
```

### 3.2 Response Schemas

**TokenResponse**:
```python
access_token: str (JWT)
refresh_token: str (JWT)
token_type: str = "bearer"
expires_in: int (seconds)
```

**UserResponse**:
```python
id: int
email: str
username: Optional[str]
full_name: Optional[str]
is_verified: bool
is_active: bool
created_at: datetime
```

### 3.3 Error Responses

- 400 Bad Request: Validation errors
- 401 Unauthorized: Invalid credentials
- 403 Forbidden: Account disabled
- 500 Internal Server Error: Server errors

## 4. Security Implementation

### 4.1 Password Security

**Hashing Algorithm**: bcrypt
- Cost factor: 12 (default)
- Automatic salt generation
- Resistant to rainbow table attacks

**Strength Requirements**:
```python
min_length = 8
requires_uppercase = True
requires_lowercase = True
requires_digit = True
requires_special = True
special_chars = "!@#$%^&*(),.?\":{}|<>"
```

### 4.2 JWT Token Security

**Access Token**:
- Expiry: 30 minutes
- Payload: `{sub: user_id, email, type: "access", exp, iat}`
- Algorithm: HS256
- Secret: 64-byte secure random key

**Refresh Token**:
- Expiry: 7 days
- Payload: `{sub: user_id, type: "refresh", exp, iat}`
- Storage: SHA256 hash in database
- Revocation: Database flag

### 4.3 Token Validation Flow

```
1. Client sends request with Authorization header
2. Service extracts Bearer token
3. JWT signature verified with secret key
4. Token expiry checked
5. Token type verified (access vs refresh)
6. User ID extracted from payload
7. User existence and active status verified
8. Request proceeds with user context
```

## 5. Configuration

### 5.1 Environment Variables

From `.env` (real working configuration):

```bash
# Service
SERVICE_NAME=authentication-service
DEBUG=true
LOG_LEVEL=INFO

# Database (PostgreSQL)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/littlemonster

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT (secure key generated)
JWT_SECRET_KEY=NlR7QZYB8DJKmyLWLQypv+B6SDIkbdqhc5qLCwE6YuVhwRWHiYHL/JH7R2BvI1gOIdwSE3wRuxUlWRu38V+Zxw==
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 5.2 Configuration Loading

Using pydantic-settings for type-safe configuration:
```python
class Settings(BaseSettings):
    SERVICE_NAME: str = "authentication-service"
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET_KEY: str
    # ... other fields
    
    class Config:
        env_file = ".env"
```

## 6. Dependencies

### 6.1 External Services

**PostgreSQL** (required):
- Host: localhost / postgres (Docker)
- Port: 5432
- Database: littlemonster
- Tables: users, oauth_connections, refresh_tokens, password_reset_tokens

**Redis** (required):
- Host: localhost / redis (Docker)
- Port: 6379
- Database: 0

### 6.2 Python Packages

Core dependencies (from requirements.txt):
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- sqlalchemy==2.0.23
- psycopg2-binary==2.9.9
- PyJWT==2.8.0
- bcrypt==4.1.0
- redis==5.0.1

Shared library:
- lm-common (local package)

## 7. Deployment

### 7.1 Docker Image

**Base Image**: python:3.11-slim

**Build Process**:
1. Install system dependencies (gcc, postgresql-client)
2. Install Python dependencies
3. Install shared lm-common library
4. Copy application code
5. Expose port 8000
6. Health check configuration

**Build Command**:
```bash
docker build -t lm-auth-service:1.0.0 .
```

### 7.2 Running the Service

**Local Development**:
```bash
python -m uvicorn src.main:app --reload --port 8001
```

**Docker**:
```bash
docker run -p 8001:8000 --env-file .env lm-auth-service:1.0.0
```

**Docker Compose** (future):
```yaml
auth-service:
  build: ./services/authentication
  ports:
    - "8001:8000"
  environment:
    - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/littlemonster
    - REDIS_URL=redis://redis:6379/0
  depends_on:
    - postgres
    - redis
```

## 8. Performance

### 8.1 Metrics (Target)

From PROJECT-CHARTER.md requirements:
- Login response time: <200ms
- Token generation: <50ms
- Password hashing: <500ms
- Throughput: 100+ req/sec

### 8.2 Optimization

- Database connection pooling (10 connections)
- Redis for session caching
- Async request handling
- Connection keep-alive
- Pre-ping database connections

## 9. Monitoring

### 9.1 Health Check

**Endpoint**: `GET /health`  
**Response**:
```json
{
  "status": "healthy",
  "service": "authentication-service",
  "version": "1.0.0"
}
```

### 9.2 Logging

Structured logging via lm-common:
- Request/response logging
- Error logging with stack traces
- Authentication events
- Token operations

**Log Format** (JSON for production):
```json
{
  "time": "2025-11-01T20:00:00",
  "service": "authentication-service",
  "level": "INFO",
  "name": "src.routes.auth",
  "message": "User logged in"
}
```

## 10. Testing Strategy

### 10.1 Unit Tests

Located in `tests/`:
- Test password hashing/verification
- Test JWT generation/validation
- Test email validation
- Test password strength validation

### 10.2 Integration Tests

- Test with real PostgreSQL database
- Test with real Redis
- Test full registration flow
- Test full login flow

### 10.3 Validation

✅ POC 12 Results:
- 10/10 tests passed
- All authentication flows validated
- JWT tokens working
- Password hashing secure

## 11. Migration Notes

### From POC 12 to Production

**Unchanged** (working code):
- JWT token generation logic
- Password hashing implementation
- Database models
- Validation rules

**Enhanced**:
- FastAPI async/await
- Pydantic schema validation
- Environment-based configuration
- Docker containerization
- Structured logging
- Health checks

**Not Modified**:
- Core authentication logic (validated)
- Security mechanisms (tested)

## 12. API Documentation

Auto-generated OpenAPI docs available at:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 13. Future Technical Enhancements

1. Redis-based rate limiting
2. Prometheus metrics export
3. Distributed tracing (OpenTelemetry)
4. OAuth 2.0 providers
5. WebAuthn/FIDO2 support
6. Audit log stream to separate service

## 14. Known Limitations

1. OAuth not yet implemented (planned)
2. Email verification not yet implemented (planned)
3. No rate limiting yet (planned)
4. No brute force protection yet (planned)

## 15. Troubleshooting

**Service won't start**:
- Check DATABASE_URL is correct
- Check PostgreSQL is running
- Check database schema is deployed

**Token errors**:
- Verify JWT_SECRET_KEY is set
- Check token hasn't expired
- Verify refresh token not revoked

**Database errors**:
- Run schema: `psql -U postgres -d littlemonster -f ../../database/schemas/master-schema.sql`
- Check connection pooling
- Verify credentials
