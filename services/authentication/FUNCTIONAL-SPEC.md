# Authentication Service - Functional Specification

## Document Control
- **Version**: 1.0
- **Date**: 2025-11-01
- **Status**: Implementation Complete
- **Service**: Authentication Service

---

## 1. Purpose

Provide secure user authentication and authorization for the Little Monster platform through JWT-based authentication, password management, and OAuth integration.

## 2. Functional Requirements

### 2.1 User Registration (FR-AUTH-001)

**Description**: Allow new users to create accounts with email and password

**Inputs**:
- Email address (required, validated)
- Password (required, strength validated)
- Username (optional, unique)
- Full name (optional)

**Processing**:
1. Validate email format
2. Check email not already registered
3. Validate password strength:
   - Minimum 8 characters
   - At least one uppercase letter
   - At least one lowercase letter  
   - At least one number
   - At least one special character
4. Hash password with bcrypt
5. Create user record in database
6. Return user data (excluding password)

**Outputs**:
- User object with id, email, username, full_name, is_verified, created_at
- HTTP 201 on success
- HTTP 400 on validation failure

**Success Criteria**: POC 12 passed 10/10 registration tests

### 2.2 User Login (FR-AUTH-002)

**Description**: Authenticate users and issue JWT tokens

**Inputs**:
- Email address
- Password

**Processing**:
1. Lookup user by email
2. Verify account is active
3. Verify password hash matches
4. Generate access token (30min expiry)
5. Generate refresh token (7day expiry)
6. Store refresh token hash in database
7. Update last_login timestamp

**Outputs**:
- access_token (JWT)
- refresh_token (JWT)
- token_type: "bearer"
- expires_in: 1800 seconds

**Success Criteria**: POC 12 passed 10/10 login tests

### 2.3 Token Refresh (FR-AUTH-003)

**Description**: Issue new access token using valid refresh token

**Inputs**:
- refresh_token (JWT string)

**Processing**:
1. Verify refresh token signature and expiry
2. Check token not revoked in database
3. Verify user exists and is active
4. Generate new access token
5. Return new token with same refresh token

**Outputs**:
- New access_token
- Same refresh_token
- expires_in: 1800 seconds

**Success Criteria**: Token can be refreshed before expiry

### 2.4 User Logout (FR-AUTH-004)

**Description**: Revoke refresh token to logout user

**Inputs**:
- refresh_token to revoke

**Processing**:
1. Hash the provided token
2. Find token in database
3. Mark as revoked with timestamp
4. Return success message

**Outputs**:
- Success message
- HTTP 200

**Success Criteria**: Revoked token cannot be used for refresh

### 2.5 Password Security (FR-AUTH-005)

**Description**: Enforce strong password requirements

**Rules**:
- Minimum 8 characters length
- Must contain uppercase letter (A-Z)
- Must contain lowercase letter (a-z)
- Must contain number (0-9)
- Must contain special character (!@#$%^&*(),.?":{}|<>)

**Hashing**: bcrypt with salt (cost factor 12)

**Success Criteria**: Weak passwords rejected, strong passwords accepted

### 2.6 Email Validation (FR-AUTH-006)

**Description**: Validate email format

**Rules**:
- Standard email regex pattern
- Maximum 255 characters
- Must be unique in database

**Success Criteria**: Invalid emails rejected

## 3. Non-Functional Requirements

### 3.1 Performance
- Login response time: <200ms (target from PROJECT-CHARTER.md)
- Token generation: <50ms
- Password hashing: <500ms (bcrypt is CPU intensive)

### 3.2 Security
- Passwords never stored in plaintext
- JWT tokens signed with secret key
- Refresh tokens stored as SHA256 hashes
- Token expiry enforced
- Failed login attempts logged

### 3.3 Scalability
- Stateless authentication (JWT)
- Database connection pooling (10 connections)
- Redis for session caching
- Horizontal scaling ready

### 3.4 Availability
- Health check endpoint for monitoring
- Graceful startup and shutdown
- Database retry logic
- No single point of failure

## 4. API Specification

### 4.1 Endpoints

| Method | Path | Description | Auth Required |
|--------|------|-------------|---------------|
| POST | /auth/register | Create new user | No |
| POST | /auth/login | Login and get tokens | No |
| POST | /auth/refresh | Refresh access token | No |
| POST | /auth/logout | Revoke refresh token | No |
| GET | /health | Health check | No |
| GET | /docs | API documentation | No |

### 4.2 Authentication Flow

```
1. User Registration:
   Client -> POST /auth/register -> Service validates -> Database stores -> Return user

2. User Login:
   Client -> POST /auth/login -> Service validates -> Generate tokens -> Return tokens

3. Protected Resource Access:
   Client -> Request with Bearer token -> Other service validates token -> Process request

4. Token Refresh:
   Client -> POST /auth/refresh -> Service validates -> Generate new access token -> Return token

5. Logout:
   Client -> POST /auth/logout -> Service revokes refresh token -> Return success
```

## 5. Data Model

### 5.1 User
- id: integer (primary key)
- email: string (unique, indexed)
- username: string (unique, indexed)
- password_hash: string (nullable for OAuth users)
- full_name: string
- is_verified: boolean (default false)
- is_active: boolean (default true)
- created_at: timestamp
- updated_at: timestamp
- last_login: timestamp

### 5.2 RefreshToken
- id: integer (primary key)
- user_id: integer (foreign key)
- token_hash: string (unique, indexed)
- expires_at: timestamp
- created_at: timestamp
- revoked: boolean (default false)
- revoked_at: timestamp

## 6. Integration Points

### 6.1 Dependencies
- PostgreSQL database (shared)
- Redis cache (shared)
- lm-common library (JWT, password utils)

### 6.2 Consumers
- All other microservices verify tokens
- Web application for user interface
- Mobile apps (future)

## 7. Testing Requirements

### 7.1 Unit Tests
- Password hashing and verification
- JWT token generation and validation
- Email validation
- Password strength validation

### 7.2 Integration Tests
- User registration flow
- Login flow
- Token refresh flow
- Logout flow

### 7.3 Security Tests
- SQL injection prevention
- XSS prevention
- Brute force protection
- Token tampering detection

## 8. Success Criteria

✅ All requirements met:
- User can register with email/password
- User can login and receive tokens
- Tokens can be refreshed before expiry
- Tokens can be revoked on logout
- Passwords securely hashed
- Strong password enforcement
- POC 12 validation: 10/10 tests passed

## 9. Future Enhancements

1. OAuth 2.0 integration (Google, Facebook, Microsoft)
2. Email verification workflow
3. Password reset workflow
4. Two-factor authentication (2FA)
5. Rate limiting per IP
6. Account lockout after failed attempts
7. Audit logging
8. GDPR compliance features
