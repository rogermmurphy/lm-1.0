# Phase 5: Gamification - Ready to Implement

## Status
Schema deployed ✅ - Service implementation needed

## What's Been Done

### Database Schema ✅
- **Schema 010**: DEPLOYED (4 tables)
  - `user_points` - User points, levels, streaks
  - `achievements` - Earned achievements/badges
  - `leaderboards` - Rankings (global, class, weekly, monthly)
  - `point_transactions` - Audit trail of point changes

### Database Functions ✅
- `award_points()` - Award points and update level
- `update_streak()` - Update daily activity streak
- Auto-level calculation (1-10 based on points)

## Implementation Pattern (Copy Phase 4)

### Service Structure Needed
```
services/gamification/
├── Dockerfile (copy from Phase 4, change port to 8011)
├── requirements.txt (same as Phase 4)
├── .env (SERVICE_PORT=8011)
├── test_service.py
└── src/
    ├── __init__.py
    ├── main.py (FastAPI with CORS)
    ├── config.py (port 8011)
    ├── models.py (Pydantic models)
    └── routes/
        ├── __init__.py
        ├── points.py (award, get points, get transactions)
        ├── achievements.py (get, award achievements)
        └── leaderboards.py (get rankings, update)
```

### API Endpoints to Implement (~12 endpoints)

**Points Routes (points.py):**
- GET /api/points - Get user's points and level
- POST /api/points/award - Award points to user
- GET /api/points/transactions - Get point history
- POST /api/points/streak - Update daily streak

**Achievements Routes (achievements.py):**
- GET /api/achievements - Get user's achievements
- POST /api/achievements - Award achievement
- GET /api/achievements/available - Get available achievements

**Leaderboard Routes (leaderboards.py):**
- GET /api/leaderboards/global - Global leaderboard
- GET /api/leaderboards/class/{class_id} - Class leaderboard
- GET /api/leaderboards/weekly - Weekly leaderboard
- GET /api/leaderboards/monthly - Monthly leaderboard
- POST /api/leaderboards/update - Update rankings

### Quick Implementation Steps

1. **Copy Phase 4 files as template**:
   ```bash
   # Copy structure from social-collaboration
   cp services/social-collaboration/requirements.txt services/gamification/
   cp services/social-collaboration/Dockerfile services/gamification/
   # Update port to 8011 in all files
   ```

2. **Create models.py** with Pydantic models for:
   - UserPoints, PointTransaction
   - Achievement, AchievementCreate
   - Leaderboard, LeaderboardEntry

3. **Create route files** (copy pattern from Phase 4):
   - points.py - Use psycopg2 to call award_points() function
   - achievements.py - INSERT/SELECT from achievements table
   - leaderboards.py - SELECT with ORDER BY for rankings

4. **Create main.py** with CORS (exact copy of Phase 4 pattern)

5. **Add to docker-compose.yml**:
   ```yaml
   gamification-service:
     build: ./services/gamification
     ports:
       - "8011:8011"
     environment:
       - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/littlemonster
   ```

6. **Test with test_service.py**

7. **Create UI page** at `/dashboard/leaderboard`

8. **Test with Playwright**

## Key Features to Implement

### Points System
- Award points for activities (study, complete assignments, etc.)
- Track point transactions
- Auto-calculate user level (1-10)
- Display points/level in UI

### Achievements
- Define achievement types (first_note, study_streak_7, etc.)
- Award achievements automatically
- Display badges in UI

### Leaderboards
- Global rankings
- Class-specific rankings
- Time-based (weekly/monthly)
- Real-time updates

### Streaks
- Track consecutive days of activity
- Award bonus points for streaks
- Display streak counter in UI

## Estimated Time
- Service implementation: 15 minutes (following Phase 4 pattern)
- UI implementation: 10 minutes
- Testing: 5 minutes
- **Total**: ~30 minutes

## Files to Create
1. services/gamification/requirements.txt
2. services/gamification/.env
3. services/gamification/Dockerfile
4. services/gamification/src/__init__.py
5. services/gamification/src/config.py
6. services/gamification/src/models.py
7. services/gamification/src/main.py
8. services/gamification/src/routes/__init__.py
9. services/gamification/src/routes/points.py
10. services/gamification/src/routes/achievements.py
11. services/gamification/src/routes/leaderboards.py
12. services/gamification/test_service.py
13. views/web-app/src/app/dashboard/leaderboard/page.tsx
14. Update: views/web-app/src/components/Navigation.tsx (add Leaderboard link)
15. Update: docker-compose.yml (add gamification service)

## Current System State
- **Services Running**: 10 (Phase 4 complete)
- **Database Tables**: 35 (31 + 4 new from Phase 5)
- **Next Service Port**: 8011
- **Pattern Established**: Phases 1-4 provide complete template

## Next Steps
1. Create service files (copy Phase 4 pattern)
2. Implement 12 API endpoints
3. Test backend
4. Create leaderboard UI page
5. Test with Playwright
6. Document completion

**Status**: Schema deployed, ready for service implementation
