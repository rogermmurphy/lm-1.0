# POC 8: Async Job Processing
## Background Presentation Generation with Database Tracking

**Goal**: Handle long-running presentation generation asynchronously  
**Time**: 1-2 days  
**Priority**: HIGH

---

## Problem Solved

**Issue**: Presenton takes 10-20 minutes to generate presentations on CPU  
**Solution**: Queue jobs, return immediately, process in background

---

## Architecture

```
User: "Create presentation"
    ↓
LLM → Agent → presentation_tool()
    ↓
Creates database record (status='pending', subject='default')
    ↓
Queues job in Redis
    ↓
Returns immediately: "Started generating..."
    ↓
(User can continue chatting)
    ↓
Background Worker picks up job
    ↓
Calls Presenton API (takes 10-20 mins)
    ↓
Updates database: status='complete', presenton_url=...
    ↓
UI shows new presentation in "Unorganized" (subject='default')
```

---

## Components

### 1. Database Table
**File**: `schema.sql`

**Fields**:
- `id` - Job ID
- `topic` - Presentation topic
- `status` - pending, processing, complete, error
- `subject` - default (unorganized) or biology, math, etc.
- `presenton_id` - ID from Presenton API
- `presenton_url` - Link to view/edit
- `created_at`, `completed_at` - Timestamps

### 2. Async Tool
**File**: `async_presentation_tool.py`

**Functions**:
- `create_presentation_async()` - Queue job, return immediately
- `get_job_status()` - Check job status
- `list_presentations()` - Get all presentations (or filter by subject)
- `update_subject()` - Organize presentation (default → biology)

### 3. Background Worker
**File**: `worker.py`

**What it does**:
- Runs continuously
- Pulls jobs from Redis queue
- Calls Presenton API
- Updates database with results
- Handles errors

---

## Setup

### Step 1: Create Database Table (1 minute)
```bash
# Connect to PostgreSQL
docker exec -it lm-postgres psql -U postgres -d lm_dev

# Run schema
\i poc/08-async-jobs/schema.sql
```

Or directly:
```bash
docker exec -it lm-postgres psql -U postgres -d lm_dev -f poc/08-async-jobs/schema.sql
```

### Step 2: Install Dependencies
```bash
cd poc/08-async-jobs
pip install psycopg2-binary redis
```

### Step 3: Start Worker (in separate terminal)
```bash
python worker.py
```

Leave this running - it processes jobs as they come in.

---

## Usage

### Queue a Presentation Job
```python
from async_presentation_tool import AsyncPresentationTool

tool = AsyncPresentationTool()

# Create job
result = tool.create_presentation_async(
    topic="Photosynthesis for Biology Test",
    user_id="user123",
    n_slides=5
)

print(result)
# {
#   'job_id': 'uuid...',
#   'status': 'pending',
#   'message': 'Started generating...',
#   'check_status': '/api/presentations/uuid'
# }
```

### Check Job Status
```python
status = tool.get_job_status(job_id)
# {
#   'job_id': '...',
#   'topic': '...',
#   'status': 'complete',
#   'presenton_url': '/presentation?id=...'
# }
```

### List Unorganized Presentations
```python
presentations = tool.list_presentations(subject='default')
# Shows all presentations that haven't been organized yet
```

### Organize Presentation
```python
tool.update_subject(job_id, 'biology')
# Moves from 'default' to 'biology' category
```

---

## Integration with Agent

### Updated presentation_tool():
```python
def presentation_tool(topic: str, user_id: str) -> str:
    """Create presentation asynchronously"""
    from async_presentation_tool import AsyncPresentationTool
    
    tool = AsyncPresentationTool()
    result = tool.create_presentation_async(topic, user_id, n_slides=5)
    
    return f"""Started creating presentation on "{topic}"!

Job ID: {result['job_id']}
Status: {result['status']}

The presentation will be ready in 10-20 minutes.
You can check status or continue chatting - I'll let you know when it's done!

Check progress: /api/presentations/{result['job_id']}"""
```

**LLM returns immediately**, user can keep chatting!

---

## UI Queries

### Show Unorganized Presentations
```sql
SELECT * FROM presentation_jobs 
WHERE subject = 'default' AND status = 'complete'
ORDER BY created_at DESC;
```

### Show by Subject
```sql
SELECT * FROM presentation_jobs 
WHERE subject = 'biology' AND status = 'complete'
ORDER BY created_at DESC;
```

### Show Pending Jobs
```sql
SELECT * FROM presentation_jobs 
WHERE status IN ('pending', 'processing')
ORDER BY created_at ASC;
```

---

## Benefits

✅ **Instant Response**: User gets immediate confirmation  
✅ **Non-Blocking**: Can continue chatting while job processes  
✅ **Tracking**: All jobs stored in database  
✅ **Organization**: Default subject until user organizes  
✅ **Scalable**: Can run multiple workers  
✅ **Reliable**: Redis queue ensures jobs don't get lost

---

## Testing

### Test 1: Create Job
```bash
python async_presentation_tool.py
```

Should:
- Create database record
- Queue in Redis
- Return job ID immediately

### Test 2: Process Job
```bash
# Terminal 1: Start worker
python worker.py

# Terminal 2: Create job
python async_presentation_tool.py
```

Watch worker process the job!

### Test 3: Check Status
Query database or use `get_job_status(job_id)`

---

## Next Steps

1. Integrate with your agent (replace sync presentation_tool)
2. Add API endpoints for job status
3. Build UI to show presentations by subject
4. Add webhooks for job completion notifications

---

**Status**: Async job architecture ready to implement  
**Files**: schema.sql, async_presentation_tool.py, worker.py
