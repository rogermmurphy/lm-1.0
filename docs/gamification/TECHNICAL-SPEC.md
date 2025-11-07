# Little Monster GPA - Gamification System Technical Specification

## Document Information
- **Version**: 1.0
- **Last Updated**: November 6, 2025
- **Status**: Draft
- **Related Documents**:
  - `FUNCTIONAL-SPEC.md`
  - `database/schemas/010_gamification.sql`
  - `services/gamification/README.md`

---

## 1. System Architecture

### 1.1 Components
```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Monster      │  │ Customization│  │ Point        │ │
│  │ Display      │  │ Modal        │  │ Tracker      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↓ HTTP/REST
┌─────────────────────────────────────────────────────────┐
│              Gamification Service (FastAPI)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Points       │  │ Achievements │  │ Avatar       │ │
│  │ Manager      │  │ Manager      │  │ Manager      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
        ↓                    ↓                    ↓
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ PostgreSQL  │    │ Redis Cache │    │ AI Image    │
│ Database    │    │             │    │ Generation  │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 1.2 Technology Stack
- **Backend**: Python 3.11+, FastAPI
- **Database**: PostgreSQL 15+ (existing)
- **Cache**: Redis 7+ (existing)
- **AI Image**: AWS Bedrock (Stable Diffusion) or DALL-E 3
- **Queue**: Redis Queue for async AI generation
- **Storage**: AWS S3 or local filesystem for generated images

---

## 2. Database Schema

### 2.1 Monster Avatars Table
```sql
CREATE TABLE monster_avatars (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    monster_name VARCHAR(50) NOT NULL,
    base_color VARCHAR(20) DEFAULT 'orange',
    customizations JSONB DEFAULT '{}',
    current_scene_level INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id)
);

-- customizations JSONB structure:
-- {
--   "accessories": ["glasses", "hat"],
--   "clothing": ["tshirt_blue"],
--   "features": ["claws"],
--   "patterns": []
-- }
```

### 2.2 Generated Scenes Table
```sql
CREATE TABLE generated_scenes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    monster_avatar_id INTEGER NOT NULL REFERENCES monster_avatars(id) ON DELETE CASCADE,
    scene_level INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    prompt_used TEXT,
    generation_timestamp TIMESTAMP DEFAULT NOW(),
    filesize_bytes INTEGER,
    UNIQUE(user_id, scene_level)
);

CREATE INDEX idx_scenes_user ON generated_scenes(user_id);
CREATE INDEX idx_scenes_level ON generated_scenes(scene_level);
```

### 2.3 Point History Table  
```sql
CREATE TABLE point_transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    points_earned INTEGER NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    activity_description TEXT,
    multiplier DECIMAL(3,2) DEFAULT 1.00,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_points_user ON point_transactions(user_id);
CREATE INDEX idx_points_created ON point_transactions(created_at DESC);
```

### 2.4 Unlockable Items Table
```sql
CREATE TABLE customization_items (
    id SERIAL PRIMARY KEY,
    item_type VARCHAR(20) NOT NULL, -- 'accessory', 'clothing', 'feature', 'color'
    item_name VARCHAR(50) NOT NULL,
    item_code VARCHAR(50) NOT NULL UNIQUE,
    unlock_requirement VARCHAR(50), -- 'free', 'points_100', 'achievement_xyz'
    is_premium BOOLEAN DEFAULT FALSE,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_unlocked_items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    item_id INTEGER NOT NULL REFERENCES customization_items(id) ON DELETE CASCADE,
    unlocked_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, item_id)
);
```

---

## 3. API Endpoints

### 3.1 Monster Avatar Management

#### GET /api/gamification/monster
Get user's current monster configuration and stats
```json
Response:
{
  "monster_name": "Dave",
  "base_color": "orange",
  "customizations": {
    "accessories": ["glasses"],
    "clothing": ["tshirt_blue"],
    "features": ["claws"]
  },
  "current_scene_level": 2,
  "current_scene_url": "/scenes/user123_level2.png",
  "total_points": 750,
  "next_milestone": 1000,
  "progress_percent": 75
}
```

#### PUT /api/gamification/monster
Update monster customizations
```json
Request:
{
  "monster_name": "Dave",
  "base_color": "orange",
  "customizations": {
    "accessories": ["glasses", "hat"],
    "clothing": ["dress_red"],
    "features": ["claws", "wings"]
  }
}

Response:
{
  "success": true,
  "monster": { ... },
  "needs_scene_regeneration": true
}
```

### 3.2 Points Management

#### POST /api/gamification/points/award
Award points for activity (internal API, authenticated)
```json
Request:
{
  "user_id": 123,
  "activity_type": "flashcard_session",
  "points": 10,
  "description": "Completed Biology flashcard set",
  "metadata": {
    "session_id": 456,
    "cards_completed": 25
  }
}

Response:
{
  "transaction_id": 789,
  "new_total": 760,
  "milestone_reached": false,
  "streak_bonus_applied": true
}
```

#### GET /api/gamification/points/history
Get point transaction history
```json
Query params: ?limit=50&offset=0

Response:
{
  "total_points": 760,
  "transactions": [
    {
      "id": 789,
      "points": 10,
      "activity_type": "flashcard_session",
      "description": "Completed Biology flashcard set",
      "multiplier": 1.10,
      "created_at": "2025-11-06T10:30:00Z"
    }
  ],
  "page": 1,
  "total_pages": 3
}
```

### 3.3 Scene Generation

#### POST /api/gamification/scenes/generate
Trigger AI scene generation (async)
```json
Request:
{
  "scene_level": 3,
  "regenerate": false
}

Response:
{
  "job_id": "gen_abc123",
  "status": "queued",
  "estimated_time": 25
}
```

#### GET /api/gamification/scenes/status/{job_id}
Check generation status
```json
Response:
{
  "job_id": "gen_abc123",
  "status": "completed", // or "queued", "processing", "failed"
  "image_url": "/scenes/user123_level3.png",
  "generated_at": "2025-11-06T10:35:00Z"
}
```

### 3.4 Customization Shop

#### GET /api/gamification/shop/items
Get available customization items
```json
Query params: ?type=accessory&unlocked_only=false

Response:
{
  "items": [
    {
      "id": 1,
      "type": "accessory",
      "name": "Scholar Glasses",
      "code": "glasses_scholar",
      "unlock_requirement": "achievement_100_flashcards",
      "is_unlocked": true,
      "is_equipped": false,
      "preview_url": "/items/glasses_scholar.png"
    }
  ]
}
```

#### POST /api/gamification/shop/unlock
Unlock an item with points
```json
Request:
{
  "item_id": 5,
  "spend_points": 100
}

Response:
{
  "success": true,
  "item_unlocked": { ... },
  "remaining_points": 660
}
```

---

## 4. AI Image Generation Implementation

### 4.1 Service Selection
**Primary**: AWS Bedrock with Stable Diffusion SDXL
- Already integrated in LLM service
- Cost-effective
- Fast generation (15-20 seconds)
- Good quality for cartoon style

**Alternative**: OpenAI DALL-E 3
- Higher quality
- Higher cost
- Fallback if Bedrock unavailable

### 4.2 Generation Pipeline
```python
async def generate_monster_scene(
    user_id: int,
    scene_level: int,
    monster_config: dict
) -> str:
    """
    1. Build prompt from monster config + scene level
    2. Submit to AI generation queue
    3. Monitor generation progress
    4. Post-process image (resize, optimize)
    5. Upload to storage
    6. Update database with URL
    7. Notify user via WebSocket
    """
    pass
```

### 4.3 Prompt Engineering
**Base Template**:
```
A cute, friendly cartoon monster in an educational setting.
Physical description: [COLOR] body, round/chubby build, big friendly hands, 
expressive face.
Wearing: [ACCESSORIES], [CLOTHING], [FEATURES]
Scene: [SCENE_DESCRIPTION based on level]
Art style: Modern digital illustration, vibrant colors, suitable for educational 
app, G-rated content. Pixar-like quality.
```

**Scene Descriptions by Level**:
- Level 0: "sitting at a simple desk in a cozy bedroom"
- Level 1: "in a study room surrounded by colorful textbooks"
- Level 2: "in a grand library with tall bookshelves"
- Level 3: "teaching a class full of smaller monster students"
- Level 4: "walking across a beautiful university campus"
- Level 5: "at a graduation ceremony wearing a cap and gown"
- Level 6: "in a hall of fame with trophies and awards"

### 4.4 Image Processing
```python
def process_generated_image(raw_image: bytes) -> bytes:
    """
    1. Validate image (no inappropriate content)
    2. Resize to target dimensions
    3. Compress (WebP format, 85% quality)
    4. Add watermark (optional)
    5. Generate thumbnails (200x200, 512x512)
    """
    pass
```

---

## 5. Caching Strategy

### 5.1 Redis Cache Structure
```python
# Monster config cache (1 hour TTL)
CACHE_KEY = f"monster:user:{user_id}:config"
VALUE = json.dumps(monster_config)

# Points cache (real-time, 5 min TTL)
CACHE_KEY = f"points:user:{user_id}:total"
VALUE = str(total_points)

# Scene URL cache (24 hour TTL)
CACHE_KEY = f"scene:user:{user_id}:level:{level}"
VALUE = image_url
```

### 5.2 Cache Invalidation
- Monster updated → Invalidate monster config cache
- Points awarded → Invalidate points cache, update in background
- Scene generated → Update scene cache
- User customizes → Trigger scene regeneration job

---

## 6. Real-Time Updates

### 6.1 WebSocket Events
```javascript
// Point awarded event
{
  "event": "points_awarded",
  "data": {
    "points": 10,
    "new_total": 760,
    "activity": "flashcard_session",
    "milestone_reached": false
  }
}

// Milestone reached event
{
  "event": "milestone_reached",
  "data": {
    "old_level": 2,
    "new_level": 3,
    "points_required": 1000,
    "scene_generation_started": true,
    "job_id": "gen_abc123"
  }
}

// Scene ready event
{
  "event": "scene_generated",
  "data": {
    "scene_level": 3,
    "image_url": "/scenes/user123_level3.png",
    "celebration_animation": true
  }
}
```

---

## 7. Performance Optimization

### 7.1 Image Delivery
- **CDN**: Serve generated scenes via CloudFront/Cloudflare
- **Lazy Loading**: Load scenes only when visible
- **Progressive**: Show low-res placeholder, upgrade to full
- **Preloading**: Prefetch next milestone scene template

### 7.2 Database Queries
```sql
-- Optimized point total query
SELECT SUM(points_earned * multiplier) as total
FROM point_transactions
WHERE user_id = $1;

-- Cached in Redis, updated on transactions

-- Recent activity query (with index)
SELECT * FROM point_transactions
WHERE user_id = $1
ORDER BY created_at DESC
LIMIT 10;
```

### 7.3 Rate Limiting
- Scene generation: 1 request per 5 minutes per user
- Customization updates: 10 requests per minute per user
- Shop unlocks: 20 requests per minute per user

---

## 8. AI Generation Queue System

### 8.1 Redis Queue Implementation
```python
from rq import Queue
from redis import Redis

redis_conn = Redis(host='localhost', port=6379)
scene_queue = Queue('scene_generation', connection=redis_conn)

# Enqueue job
job = scene_queue.enqueue(
    generate_scene_task,
    user_id=123,
    scene_level=3,
    monster_config={...},
    job_timeout='5m'
)
```

### 8.2 Worker Configuration
- **Workers**: 4 concurrent scene generation workers
- **Timeout**: 5 minutes per job
- **Retry**: 2 retries on failure
- **Priority**: Premium users get higher priority

### 8.3 Job Status Tracking
```python
class SceneGenerationJob:
    id: str
    user_id: int
    status: str  # queued, processing, completed, failed
    progress: int  # 0-100
    error_message: Optional[str]
    image_url: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
```

---

## 9. Security Considerations

### 9.1 Input Validation
```python
from pydantic import BaseModel, validator

class MonsterCustomization(BaseModel):
    accessories: List[str] = []
    clothing: List[str] = []
    features: List[str] = []
    
    @validator('accessories')
    def validate_accessories(cls, v):
        # Max 5 accessories
        if len(v) > 5:
            raise ValueError("Maximum 5 accessories allowed")
        # Must be valid item codes
        valid_items = get_valid_accessory_codes()
        for item in v:
            if item not in valid_items:
                raise ValueError(f"Invalid accessory: {item}")
        return v
```

### 9.2 Point Transaction Integrity
```python
async def award_points_atomic(
    user_id: int,
    points: int,
    activity_type: str
) -> int:
    """
    Atomic point transaction with rollback on failure
    """
    async with db.transaction():
        # Insert transaction record
        transaction = await db.insert_point_transaction(...)
        
        # Update cached total
        new_total = await update_point_cache(user_id, points)
        
        # Check for milestone
        if milestone_reached(new_total):
            await trigger_scene_generation(user_id, new_level)
        
        return new_total
```

### 9.3 Content Safety
```python
def validate_ai_generated_content(image: bytes) -> bool:
    """
    1. Run through AWS Rekognition moderation
    2. Check for inappropriate content
    3. Verify educational appropriateness
    4. Flag for human review if uncertain
    """
    pass
```

---

## 10. Frontend Implementation

### 10.1 Monster Display Component
```typescript
interface MonsterDisplayProps {
  size?: 'small' | 'medium' | 'large';
  interactive?: boolean;
  showPoints?: boolean;
}

const MonsterDisplay: React.FC<MonsterDisplayProps> = ({
  size = 'medium',
  interactive = true,
  showPoints = true
}) => {
  const { monster, points, loading } = useMonster();
  
  return (
    <div className="monster-container">
      <div className="scene-background">
        <img src={monster.currentSceneUrl} alt="Monster scene" />
      </div>
      <div className="monster-avatar">
        {/* Rendered monster with customizations */}
      </div>
      {showPoints && (
        <div className="points-display">
          <span className="points-value">{points}</span>
          <ProgressBar current={points} next={monster.nextMilestone} />
        </div>
      )}
    </div>
  );
};
```

### 10.2 Customization Modal
```typescript
const CustomizationModal: React.FC = () => {
  const [selectedTab, setSelectedTab] = useState('accessories');
  const { monster, updateCustomization } = useMonster();
  const { availableItems, lockedItems } = useShop();
  
  const handleItemSelect = async (item: CustomizationItem) => {
    if (item.isLocked) {
      // Show unlock prompt
      return;
    }
    
    await updateCustomization({
      ...monster.customizations,
      [selectedTab]: [...monster.customizations[selectedTab], item.code]
    });
  };
  
  return (
    <Modal>
      <Tabs>
        <Tab label="Accessories" />
        <Tab label="Clothing" />
        <Tab label="Features" />
        <Tab label="Colors" />
      </Tabs>
      <ItemGrid items={availableItems} onSelect={handleItemSelect} />
      <PreviewPanel monster={monster} />
    </Modal>
  );
};
```

### 10.3 Point Animation
```typescript
const PointsAnimation: React.FC<{points: number}> = ({ points }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="points-earned"
    >
      +{points}
    </motion.div>
  );
};
```

---

## 11. Integration Points

### 11.1 Study Activity Integration
Each study feature calls gamification service after completion:

```python
# In flashcard service
async def complete_flashcard_session(session_id: int, user_id: int):
    # Complete the session
    session = await mark_session_complete(session_id)
    
    # Award points
    await gamification_client.award_points(
        user_id=user_id,
        activity_type="flashcard_session",
        points=10,
        metadata={"cards_completed": session.card_count}
    )
```

### 11.2 Authentication Service
```python
# In auth service - daily login bonus
async def login_success(user_id: int):
    # Check if first login today
    last_login = await get_last_login(user_id)
    if is_new_day(last_login):
        await gamification_client.award_points(
            user_id=user_id,
            activity_type="daily_login",
            points=5
        )
```

---

## 12. Deployment Configuration

### 12.1 Environment Variables
```bash
# AI Generation
AI_IMAGE_PROVIDER=bedrock  # or openai
BEDROCK_REGION=us-east-1
BEDROCK_MODEL_ID=stability.stable-diffusion-xl-v1

# Storage
SCENE_STORAGE_TYPE=s3  # or filesystem
S3_BUCKET_NAME=lm-monster-scenes
S3_REGION=us-east-1

# Queue
REDIS_QUEUE_HOST=localhost
REDIS_QUEUE_PORT=6379
SCENE_GENERATION_WORKERS=4

# Performance
MAX_SCENE_CACHE_SIZE_MB=1000
SCENE_COMPRESSION_QUALITY=85
```

### 12.2 Docker Service
```yaml
# In docker-compose.yml
gamification:
  build: ./services/gamification
  environment:
    - DATABASE_URL=${DATABASE_URL}
    - REDIS_URL=${REDIS_URL}
    - AI_IMAGE_PROVIDER=bedrock
  depends_on:
    - postgres
    - redis
  ports:
    - "8011:8011"

# Scene generation workers
scene-worker:
  build: ./services/gamification
  command: python -m src.workers.scene_generator
  environment:
    - REDIS_URL=${REDIS_URL}
    - AI_IMAGE_PROVIDER=bedrock
  deploy:
    replicas: 4
```

---

## 13. Testing Strategy

### 13.1 Unit Tests
```python
def test_award_points():
    """Test point transaction creation"""
    pass

def test_milestone_detection():
    """Test milestone triggering at thresholds"""
    pass

def test_customization_validation():
    """Test invalid customization rejection"""
    pass
```

### 13.2 Integration Tests
```python
async def test_complete_monster_flow():
    """
    1. Create user
    2. Create monster
    3. Award points
    4. Check milestone trigger
    5. Verify scene generation queued
    6. Verify scene created
    """
    pass
```

### 13.3 Load Tests
- 1000 concurrent users earning points
- 100 simultaneous scene generations
- Response time targets: p95 <200ms for points, <30s for scenes

---

## 14. Monitoring & Observability

### 14.1 Metrics to Track
- Points awarded per minute
- Scene generation queue length
- Scene generation success rate
- Average generation time
- Cache hit rates
- Monster customization frequency

### 14.2 Alerts
- Scene generation failure rate >5%
- Queue length >100 pending jobs
- Generation time >60 seconds
- Cache service unavailable

---

## 15. Migration Plan

### 15.1 Phase 1: Core Infrastructure
1. Deploy gamification database tables
2. Set up Redis queue for scene generation
3. Implement basic points API
4. Create monster avatar CRUD

### 15.2 Phase 2: AI Integration
1. Integrate Bedrock scene generation
2. Implement generation queue workers
3. Set up S3 storage for scenes
4. Test end-to-end generation

### 15.3 Phase 3: Frontend
1. Create monster display component
2. Build customization modal
3. Implement point animations
4. Add milestone notifications

### 15.4 Phase 4: Social Features
1. Leaderboards
2. Achievements
3. Monster showcase
4. Social sharing

---

## 16. Rollback Strategy

If issues arise:
1. Disable scene generation, use default avatars
2. Continue awarding points (tracked in database)
3. Generate scenes in batch during off-hours
4. Gradually re-enable real-time generation

---

## 17. Cost Estimation

### 17.1 AI Generation Costs
**Bedrock Stable Diffusion SDXL**:
- $0.04 per image (1024x1024)
- Estimated usage: 10K images/day initially
- Monthly cost: ~$12,000

**Optimization**:
- Cache scenes aggressively
- Only regenerate when customizations change
- Use lower quality for mobile
- Expected optimized cost: ~$3,000/month

### 17.2 Storage Costs
**S3 Storage**:
- Average 500KB per scene
- 7 scenes per user average
- 100K users = 350GB
- S3 cost: ~$8/month

---

## 18. Success Criteria

### 18.1 Technical Success
- ✅ 99.9% uptime for points API
- ✅ <200ms p95 response time
- ✅ <30 second scene generation
- ✅ 95%+ scene generation success rate
- ✅ Zero point transaction loss

### 18.2 User Experience Success
- ✅ Smooth point animations
- ✅ Instant customization preview
- ✅ Clear milestone progress
- ✅ Engaging monster personality

---

## Approval & Sign-off

**Technical Lead**: ___________________ Date: ___________

**DevOps Engineer**: ___________________ Date: ___________

**QA Lead**: ___________________ Date: ___________
