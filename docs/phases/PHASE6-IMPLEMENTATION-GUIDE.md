**Last Updated:** November 4, 2025

# Phase 6 Implementation Guide - Study Sessions & Analytics

## Quick Reference

**Service**: study-analytics  
**Port**: 8012  
**Database Schema**: 011_study_analytics.sql (✅ Deployed)  
**Status**: In Progress - Service Implementation

---

## Implementation Progress

### ✅ Completed
- [x] Implementation plan created
- [x] Database schema designed and deployed
- [x] Service structure created
- [x] requirements.txt created
- [x] .env configuration created
- [x] config.py implemented
- [x] models.py implemented

### 🔄 In Progress
- [ ] Implement session_service.py
- [ ] Implement sessions.py routes
- [ ] Implement performance_service.py
- [ ] Implement performance.py routes
- [ ] Implement goal_service.py
- [ ] Implement goals.py routes
- [ ] Implement report_service.py
- [ ] Implement reports.py routes
- [ ] Create main.py with FastAPI app
- [ ] Create Dockerfile
- [ ] Create test_service.py
- [ ] Test all 12 endpoints
- [ ] Add to docker-compose.yml
- [ ] Create UI pages
- [ ] Test with Playwright
- [ ] Document completion

---

## Service Architecture

### Route Modules (4 files)
1. **sessions.py** - 4 endpoints for session management
2. **performance.py** - 3 endpoints for performance analytics
3. **goals.py** - 5 endpoints for goal management
4. **reports.py** - 3 endpoints for report generation

### Service Modules (4 files)
1. **session_service.py** - Session tracking logic
2. **performance_service.py** - Performance calculation logic
3. **goal_service.py** - Goal management logic
4. **report_service.py** - Report generation logic

---

## API Endpoints Summary

### Sessions Routes (4 endpoints)
```
POST   /api/analytics/sessions/start              - Start study session
PUT    /api/analytics/sessions/{id}/end           - End study session
POST   /api/analytics/sessions/{id}/activities    - Log activity
GET    /api/analytics/sessions                    - List sessions
```

### Performance Routes (3 endpoints)
```
GET    /api/analytics/performance/overview        - Performance overview
GET    /api/analytics/performance/trends          - Performance trends
GET    /api/analytics/performance/comparison      - Compare performance
```

### Goals Routes (5 endpoints)
```
POST   /api/analytics/goals                       - Create goal
GET    /api/analytics/goals                       - List goals
PUT    /api/analytics/goals/{id}                  - Update goal
POST   /api/analytics/goals/{id}/progress         - Record progress
DELETE /api/analytics/goals/{id}                  - Delete goal
```

### Reports Routes (3 endpoints)
```
GET    /api/analytics/reports/daily               - Daily report
GET    /api/analytics/reports/weekly              - Weekly report
GET    /api/analytics/reports/monthly             - Monthly report
```

---

## Code Templates

### Template: sessions.py (Route Module)

```python
"""
Study session management routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from datetime import date
import psycopg2
from ..config import settings
from ..models import (
    SessionStart, SessionEnd, ActivityLog,
    StudySession, SessionsListResponse, MessageResponse
)
from shared.python_common.lm_common.auth.jwt_utils import get_current_user

router = APIRouter(prefix="/sessions", tags=["sessions"])

def get_db():
    """Database connection dependency"""
    conn = psycopg2.connect(settings.database_url)
    try:
        yield conn
    finally:
        conn.close()

@router.post("/start")
async def start_session(
    session_data: SessionStart,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db)
):
    """Start a new study session"""
    # Implementation here
    pass

@router.put("/{session_id}/end")
async def end_session(
    session_id: int,
    session_data: SessionEnd,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db)
):
    """End an active study session"""
    # Implementation here
    pass

@router.post("/{session_id}/activities")
async def log_activity(
    session_id: int,
    activity: ActivityLog,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db)
):
    """Log an activity within a session"""
    # Implementation here
    pass

@router.get("", response_model=SessionsListResponse)
async def list_sessions(
    class_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = Query(50, le=100),
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db)
):
    """Get user's study sessions with filters"""
    # Implementation here
    pass
```

### Template: session_service.py (Business Logic)

```python
"""
Session management business logic
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import Optional, List, Dict, Any
import requests
from ..config import settings

class SessionService:
    """Service for managing study sessions"""
    
    def __init__(self, conn):
        self.conn = conn
    
    def start_session(self, user_id: int, class_id: Optional[int], 
                     session_type: str, focus_mode: bool, 
                     location: Optional[str]) -> Dict[str, Any]:
        """Start a new study session"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                INSERT INTO study_sessions 
                (user_id, class_id, session_type, focus_mode, location)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, start_time
            """, (user_id, class_id, session_type, focus_mode, location))
            
            result = cursor.fetchone()
            self.conn.commit()
            
            return {
                "session_id": result['id'],
                "start_time": result['start_time'],
                "message": "Study session started"
            }
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Failed to start session: {str(e)}")
        finally:
            cursor.close()
    
    def end_session(self, session_id: int, user_id: int,
                   mood_rating: Optional[int], productivity_rating: Optional[int],
                   notes: Optional[str]) -> Dict[str, Any]:
        """End an active study session"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Update session
            cursor.execute("""
                UPDATE study_sessions
                SET end_time = NOW(),
                    mood_rating = %s,
                    productivity_rating = %s,
                    notes = %s
                WHERE id = %s AND user_id = %s AND end_time IS NULL
                RETURNING id, duration_minutes
            """, (mood_rating, productivity_rating, notes, session_id, user_id))
            
            result = cursor.fetchone()
            if not result:
                raise Exception("Session not found or already ended")
            
            # Calculate points (0.5 points per minute)
            duration = result['duration_minutes'] or 0
            points = int(duration * 0.5)
            
            # Award points via gamification service
            if points > 0:
                self._award_points(user_id, points, "study_session", session_id)
            
            self.conn.commit()
            
            return {
                "session_id": session_id,
                "duration_minutes": duration,
                "points_earned": points,
                "message": "Study session ended"
            }
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Failed to end session: {str(e)}")
        finally:
            cursor.close()
    
    def _award_points(self, user_id: int, points: int, 
                     reason: str, reference_id: int):
        """Award points via gamification service"""
        try:
            response = requests.post(
                f"{settings.gamification_service_url}/api/gamification/points/award",
                json={
                    "user_id": user_id,
                    "points": points,
                    "reason": reason,
                    "reference_type": "study_session",
                    "reference_id": reference_id
                },
                timeout=5
            )
            response.raise_for_status()
        except Exception as e:
            # Log error but don't fail the session end
            print(f"Warning: Failed to award points: {e}")
```

---

## Implementation Steps

### Step 1: Implement Session Routes (Priority 1)

1. Create `services/study-analytics/src/services/session_service.py`
2. Create `services/study-analytics/src/routes/sessions.py`
3. Implement all 4 session endpoints
4. Test session start/end workflow

### Step 2: Implement Performance Routes (Priority 2)

1. Create `services/study-analytics/src/services/performance_service.py`
2. Create `services/study-analytics/src/routes/performance.py`
3. Implement performance calculation logic
4. Test performance queries

### Step 3: Implement Goal Routes (Priority 3)

1. Create `services/study-analytics/src/services/goal_service.py`
2. Create `services/study-analytics/src/routes/goals.py`
3. Implement goal CRUD operations
4. Test goal progress tracking

### Step 4: Implement Report Routes (Priority 4)

1. Create `services/study-analytics/src/services/report_service.py`
2. Create `services/study-analytics/src/routes/reports.py`
3. Implement report generation
4. Test report accuracy

### Step 5: Create Main Application

1. Create `services/study-analytics/src/main.py`
2. Set up FastAPI with CORS
3. Include all route modules
4. Add health check endpoint

### Step 6: Create Dockerfile

1. Create `services/study-analytics/Dockerfile`
2. Follow pattern from Phase 5
3. Test Docker build

### Step 7: Create Test Suite

1. Create `services/study-analytics/test_service.py`
2. Test all 12 endpoints
3. Achieve 100% pass rate

### Step 8: Add to Docker Compose

1. Update `docker-compose.yml`
2. Add study-analytics service
3. Test service startup

---

## Testing Checklist

### Session Endpoints
- [ ] POST /sessions/start - Creates session
- [ ] PUT /sessions/{id}/end - Ends session, calculates duration, awards points
- [ ] POST /sessions/{id}/activities - Logs activity
- [ ] GET /sessions - Returns filtered sessions

### Performance Endpoints
- [ ] GET /performance/overview - Returns metrics
- [ ] GET /performance/trends - Returns trend data
- [ ] GET /performance/comparison - Returns comparisons

### Goal Endpoints
- [ ] POST /goals - Creates goal
- [ ] GET /goals - Lists goals
- [ ] PUT /goals/{id} - Updates goal
- [ ] POST /goals/{id}/progress - Records progress
- [ ] DELETE /goals/{id} - Deletes goal

### Report Endpoints
- [ ] GET /reports/daily - Generates daily report
- [ ] GET /reports/weekly - Generates weekly report
- [ ] GET /reports/monthly - Generates monthly report

---

## Integration Points

### With Gamification Service (Phase 5)
- Award points when sessions end
- Trigger achievements based on analytics
- Update leaderboards with study time

### With AI Study Tools (Phase 3)
- Track test scores
- Monitor flashcard performance
- Include note usage stats

### With Class Management (Phase 1)
- Link sessions to classes
- Track study time per class
- Include assignment completion

---

## Database Functions to Use

### Auto-Calculation Functions
- `calculate_session_duration()` - Automatically calculates duration on session end
- `calculate_activity_duration()` - Automatically calculates activity metrics
- `update_goal_progress_percentage()` - Automatically calculates goal progress
- `update_goal_current_value()` - Automatically updates goal from progress

### Utility Functions
- `check_expired_goals()` - Call periodically to mark expired goals

### Views to Query
- `active_study_sessions` - Get currently active sessions
- `user_study_summary_30d` - Get 30-day summary
- `active_goals_with_progress` - Get goals with calculated progress

---

## Performance Considerations

### Query Optimization
- Use indexes for date range queries
- Limit result sets with pagination
- Cache frequently accessed data

### Point Award Optimization
- Award points asynchronously if possible
- Don't fail session end if points fail
- Log point award failures

### Report Generation
- Pre-calculate snapshots for common reports
- Use analytics_snapshots table for fast queries
- Generate complex reports asynchronously

---

## Next Steps

1. **Implement session routes first** - Most critical functionality
2. **Test session workflow** - Start → Activities → End → Points
3. **Implement remaining routes** - Performance, Goals, Reports
4. **Create comprehensive test suite** - 100% pass rate required
5. **Build UI components** - Analytics dashboard
6. **Validate with Playwright** - End-to-end testing

---

## Reference Files

- **PHASE6-IMPLEMENTATION-PLAN.md** - Complete architecture
- **database/schemas/011_study_analytics.sql** - Database schema
- **services/gamification/** - Phase 5 example (similar complexity)
- **services/social-collaboration/** - Phase 4 example (19 endpoints)
- **PHASE5-IMPLEMENTATION-GUIDE.md** - Code templates

---

## Success Criteria

- ✅ All 12 endpoints functional
- ✅ 100% test pass rate
- ✅ Points awarded for sessions
- ✅ Performance calculations accurate
- ✅ Goals track progress automatically
- ✅ Reports generate successfully
- ✅ UI displays analytics correctly
- ✅ Playwright tests pass

---

## Estimated Timeline

- **Day 1**: Session routes + testing (4 endpoints)
- **Day 2**: Performance routes + testing (3 endpoints)
- **Day 3**: Goal routes + testing (5 endpoints)
- **Day 4**: Report routes + testing (3 endpoints)
- **Day 5**: UI implementation + Playwright testing
- **Day 6**: Documentation + completion

**Total**: 6 days to complete Phase 6

---

## Notes

- Follow zero-tolerance testing: Deploy → Test → Fix → Re-test
- Use established patterns from Phases 4 & 5
- Test integrations with gamification service
- Ensure CORS is configured from the start
- Document any deviations from the plan
