# Little Monster Common Library

Shared utilities for all Little Monster microservices.

## Overview

This package provides common functionality used across all microservices:

- **Authentication**: JWT token generation/validation, password hashing
- **Database**: PostgreSQL connection and session management
- **Redis**: Caching and job queue operations
- **Logging**: Structured logging configuration

## Installation

```bash
# Install in development mode (for local development)
pip install -e .

# Install from package
pip install lm-common
```

## Usage

### Authentication - JWT Tokens

```python
from lm_common.auth import jwt_utils

# Create access token
access_token = jwt_utils.create_access_token(
    user_id=123,
    email="user@example.com"
)

# Verify access token
user_id = jwt_utils.verify_access_token(access_token)

# Create refresh token
refresh_token = jwt_utils.create_refresh_token(user_id=123)
```

### Authentication - Password Hashing

```python
from lm_common.auth import password_utils

# Hash a password
hashed = password_utils.hash_password("MyPassword123!")

# Verify password
is_valid = password_utils.verify_password("MyPassword123!", hashed)

# Validate password strength
is_strong, error = password_utils.validate_password_strength("weak")
```

### Database Access

```python
from lm_common.database import get_db_session, get_db
from sqlalchemy.orm import Session

# Context manager usage
with get_db_session() as db:
    user = db.query(User).filter(User.id == 1).first()

# FastAPI dependency usage
from fastapi import Depends

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()
```

### Redis Operations

```python
from lm_common.redis_client import cache_set, cache_get, queue_push, queue_pop

# Caching
cache_set("user:123", {"name": "John"}, expire=3600)
data = cache_get("user:123")

# Job Queue
queue_push("transcription_jobs", {"file": "audio.mp3"})
job = queue_pop("transcription_jobs", timeout=5)
```

### Logging

```python
from lm_common.logging import setup_logging, get_logger

# Setup logging for service
setup_logging(service_name="auth-service", level="INFO")

# Get logger
logger = get_logger(__name__)
logger.info("Service started")
logger.error("An error occurred", exc_info=True)
```

## Environment Variables

### Required

- `DATABASE_URL` - PostgreSQL connection string
  - Format: `postgresql://user:password@host:port/database`
  - Default: `postgresql://postgres:postgres@localhost:5432/littlemonster`

- `REDIS_URL` - Redis connection string
  - Format: `redis://host:port/db`
  - Default: `redis://localhost:6379/0`

### Authentication

- `JWT_SECRET_KEY` - Secret key for JWT signing (required in production)
  - Default: `dev-secret-key-change-in-production`

- `JWT_ALGORITHM` - JWT algorithm
  - Default: `HS256`

- `ACCESS_TOKEN_EXPIRE_MINUTES` - Access token expiration
  - Default: `30`

- `REFRESH_TOKEN_EXPIRE_DAYS` - Refresh token expiration
  - Default: `7`

### Logging

- `LOG_LEVEL` - Logging level
  - Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
  - Default: `INFO`

- `SERVICE_NAME` - Service identifier for logs
  - Default: `unknown`

- `SQL_ECHO` - Echo SQL queries
  - Options: `true`, `false`
  - Default: `false`

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=lm_common

# Format code
black lm_common/

# Lint code
flake8 lm_common/

# Type check
mypy lm_common/
```

## Code Quality

All code extracted from validated POCs:
- ✅ POC 12: Authentication (10/10 tests passed)
- ✅ POC 09: Speech-to-Text (working)
- ✅ POC 08: Async Jobs (working)

## License

MIT License - see LICENSE file for details

## Version

1.0.0 - Initial release with core utilities from validated POCs
