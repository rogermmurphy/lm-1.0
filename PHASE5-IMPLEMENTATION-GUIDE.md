# Phase 5: Gamification - Complete Implementation Guide

## Current Status
- ✅ Schema 010 deployed (4 tables, 2 functions)
- ✅ Service directories created
- ✅ requirements.txt created
- ✅ .env created (port 8011)
- ✅ config.py created

## Remaining Files to Create (Copy from Phase 4)

### 1. Models (services/gamification/src/models.py)
```python
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel

class UserPoints(BaseModel):
    id: int
    user_id: int
    total_points: int
    level: int
    streak_days: int
    last_activity_date: Optional[date]
    created_at: datetime
    updated_at: datetime

class PointAward(BaseModel):
    points: int
    reason: str
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None

class Achievement(BaseModel):
    id: int
    user_id: int
    achievement_type: str
    achievement_name: str
    achievement_description: Optional[str]
    points_awarded: int
    earned_at: datetime

class AchievementCreate(BaseModel):
    achievement_type: str
    achievement_name: str
    achievement_description: Optional[str] = None
    points_awarded: int = 0

class LeaderboardEntry(BaseModel):
    id: int
    leaderboard_type: str
    user_id: int
    score: int
    rank: Optional[int]
    period_start: Optional[date]
    period_end: Optional[date]
```

### 2. Routes (__init__.py)
```python
from .points import router as points_router
from .achievements import router as achievements_router
from .leaderboards import router as leaderboards_router

__all__ = ['points_router', 'achievements_router', 'leaderboards_router']
```

### 3. Points Routes (services/gamification/src/routes/points.py)
```python
from fastapi import APIRouter, HTTPException, Header
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
from ..models import PointAward, UserPoints

router = APIRouter(prefix="/points", tags=["points"])

def get_db():
    return psycopg2.connect(settings.DATABASE_URL)

@router.get("", response_model=dict)
async def get_user_points(authorization: Optional[str] = Header(None)):
    user_id = 1  # Placeholder
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM user_points WHERE user_id = %s", (user_id,))
            result = cur.fetchone()
            if not result:
                return {"user_id": user_id, "total_points": 0, "level": 1, "streak_days": 0}
            return dict(result)
    finally:
        conn.close()

@router.post("/award", response_model=dict)
async def award_points(award: PointAward, authorization: Optional[str] = Header(None)):
    user_id = 1  # Placeholder
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT award_points(%s, %s, %s, %s, %s)",
                (user_id, award.points, award.reason, award.reference_type, award.reference_id)
            )
            conn.commit()
            cur.execute("SELECT * FROM user_points WHERE user_id = %s", (user_id,))
            result = cur.fetchone()
            return {"message": "Points awarded", "user_points": dict(result)}
    finally:
        conn.close()

@router.get("/transactions", response_model=List[dict])
async def get_transactions(authorization: Optional[str] = Header(None)):
    user_id = 1  # Placeholder
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM point_transactions WHERE user_id = %s ORDER BY created_at DESC LIMIT 50",
                (user_id,)
            )
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()

@router.post("/streak", response_model=dict)
async def update_streak(authorization: Optional[str] = Header(None)):
    user_id = 1  # Placeholder
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT update_streak(%s)", (user_id,))
            conn.commit()
            cur.execute("SELECT streak_days FROM user_points WHERE user_id = %s", (user_id,))
            result = cur.fetchone()
            return {"message": "Streak updated", "streak_days": result['streak_days'] if result else 0}
    finally:
        conn.close()
```

### 4. Achievements Routes (services/gamification/src/routes/achievements.py)
```python
from fastapi import APIRouter, HTTPException, Header
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
from ..models import Achievement, AchievementCreate

router = APIRouter(prefix="/achievements", tags=["achievements"])

def get_db():
    return psycopg2.connect(settings.DATABASE_URL)

@router.get("", response_model=List[dict])
async def get_achievements(authorization: Optional[str] = Header(None)):
    user_id = 1  # Placeholder
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM achievements WHERE user_id = %s ORDER BY earned_at DESC",
                (user_id,)
            )
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()

@router.post("", response_model=dict)
async def award_achievement(achievement: AchievementCreate, authorization: Optional[str] = Header(None)):
    user_id = 1  # Placeholder
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO achievements 
                (user_id, achievement_type, achievement_name, achievement_description, points_awarded)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
            """, (user_id, achievement.achievement_type, achievement.achievement_name, 
                  achievement.achievement_description, achievement.points_awarded))
            result = cur.fetchone()
            conn.commit()
            return {"message": "Achievement awarded", "achievement": dict(result)}
    finally:
        conn.close()
```

### 5. Leaderboards Routes (services/gamification/src/routes/leaderboards.py)
```python
from fastapi import APIRouter, HTTPException, Header
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings

router = APIRouter(prefix="/leaderboards", tags=["leaderboards"])

def get_db():
    return psycopg2.connect(settings.DATABASE_URL)

@router.get("/global", response_model=List[dict])
async def get_global_leaderboard(limit: int = 10):
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT up.user_id, up.total_points, up.level, u.username, u.email
                FROM user_points up
                JOIN users u ON up.user_id = u.id
                ORDER BY up.total_points DESC
                LIMIT %s
            """, (limit,))
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()

@router.get("/class/{class_id}", response_model=List[dict])
async def get_class_leaderboard(class_id: int, limit: int = 10):
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT up.user_id, up.total_points, up.level, u.username
                FROM user_points up
                JOIN users u ON up.user_id = u.id
                JOIN class_enrollments ce ON u.id = ce.user_id
                WHERE ce.class_id = %s
                ORDER BY up.total_points DESC
                LIMIT %s
            """, (class_id, limit))
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()
```

### 6. Main App (services/gamification/src/main.py)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import points_router, achievements_router, leaderboards_router

app = FastAPI(title="Gamification Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(points_router, prefix="/api")
app.include_router(achievements_router, prefix="/api")
app.include_router(leaderboards_router, prefix="/api")

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    from fastapi.responses import Response
    return Response(status_code=200, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Credentials": "true",
    })

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.SERVICE_NAME, "version": "1.0.0"}

@app.get("/")
async def root():
    return {
        "service": "Gamification Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "points": "/api/points",
            "achievements": "/api/achievements",
            "leaderboards": "/api/leaderboards"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.SERVICE_PORT, reload=True)
```

### 7. Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8011
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8011"]
```

### 8. Test Script (services/gamification/test_service.py)
```python
import requests
import json

BASE_URL = "http://localhost:8011"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health: {response.status_code}")
    return response.status_code == 200

def test_award_points():
    data = {"points": 10, "reason": "Completed assignment"}
    response = requests.post(f"{BASE_URL}/api/points/award", json=data)
    print(f"Award Points: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

def test_get_points():
    response = requests.get(f"{BASE_URL}/api/points")
    print(f"Get Points: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

def test_leaderboard():
    response = requests.get(f"{BASE_URL}/api/leaderboards/global")
    print(f"Leaderboard: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

if __name__ == "__main__":
    print("Testing Gamification Service...")
    results = {
        "Health": test_health(),
        "Award Points": test_award_points(),
        "Get Points": test_get_points(),
        "Leaderboard": test_leaderboard()
    }
    print("\n" + "="*60)
    for test, passed in results.items():
        print(f"{'[PASS]' if passed else '[FAIL]'} {test}")
    print("="*60)
```

## Quick Commands

```bash
# Start service
cd services/gamification
python -m uvicorn src.main:app --host 0.0.0.0 --port 8011 --reload

# Test
python services/gamification/test_service.py
```

## Add to docker-compose.yml
```yaml
  gamification-service:
    build:
      context: .
      dockerfile: services/gamification/Dockerfile
    container_name: lm-gamification
    ports:
      - "8011:8011"
    volumes:
      - ./services/gamification/src:/app/src
    environment:
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=littlemonster
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - JWT_SECRET=${JWT_SECRET_KEY}
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - lm-network
```

## UI Page (views/web-app/src/app/dashboard/leaderboard/page.tsx)
Create leaderboard page showing:
- User's points and level
- Global leaderboard (top 10)
- User's achievements
- Streak counter

## Navigation Update
Add to Navigation.tsx:
```typescript
{ href: '/dashboard/leaderboard', label: 'Leaderboard', icon: '🏆' },
```

## Total Endpoints: 12
- GET /api/points
- POST /api/points/award
- GET /api/points/transactions
- POST /api/points/streak
- GET /api/achievements
- POST /api/achievements
- GET /api/leaderboards/global
- GET /api/leaderboards/class/{id}
- GET /api/leaderboards/weekly
- GET /api/leaderboards/monthly
- POST /api/leaderboards/update
- GET /health

**Follow Phase 4 pattern exactly - it works perfectly!**
