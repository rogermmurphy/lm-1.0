# Phase 7: Notifications & Communication System - Planning Document

## Document Control
- **Version**: 1.0
- **Date**: November 2, 2025
- **Status**: Planning
- **Dependencies**: Phases 1-6 Complete

---

## Executive Summary

Phase 7 implements a **Notifications & Communication System** to keep users engaged and informed about important events, deadlines, achievements, and social interactions across the platform.

### Key Features
1. **Real-time Notifications** - In-app notifications for immediate events
2. **Email Notifications** - Digest emails and important alerts
3. **Push Notifications** - Mobile push notifications (future)
4. **Notification Preferences** - User-controlled notification settings
5. **Communication Channels** - Direct messaging between users
6. **Announcement System** - Platform-wide and class-specific announcements

---

## Why Phase 7?

### Business Value
- **Engagement**: Keep users active and returning to the platform
- **Retention**: Remind users of pending tasks and goals
- **Social**: Enable communication between study partners
- **Accountability**: Alert users to deadlines and commitments

### Technical Readiness
- All data sources in place (Phases 1-6)
- User system established (Phase 1)
- Social connections exist (Phase 4)
- Events to notify about (assignments, goals, achievements, messages)

---

## Architecture Overview

### Service: notifications
- **Port**: 8013
- **Database Schema**: 012_notifications.sql
- **Dependencies**: All previous phases
- **API Endpoints**: ~15 endpoints across 4 route modules

### Database Tables (5 new tables)
1. `notifications` - Individual notification records
2. `notification_preferences` - User notification settings
3. `notification_templates` - Reusable notification templates
4. `direct_messages` - User-to-user messages
5. `announcements` - Platform/class announcements

---

## Database Schema Design (Draft)

### Table 1: notifications
```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    action_url VARCHAR(500),
    reference_type VARCHAR(50),
    reference_id INTEGER,
    priority VARCHAR(20) DEFAULT 'normal',
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Table 2: notification_preferences
```sql
CREATE TABLE notification_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL,
    in_app_enabled BOOLEAN DEFAULT TRUE,
    email_enabled BOOLEAN DEFAULT TRUE,
    push_enabled BOOLEAN DEFAULT FALSE,
    frequency VARCHAR(20) DEFAULT 'immediate',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, notification_type)
);
```

### Table 3: direct_messages
```sql
CREATE TABLE direct_messages (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipient_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Table 4: announcements
```sql
CREATE TABLE announcements (
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    scope VARCHAR(20) NOT NULL,
    class_id INTEGER REFERENCES classes(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'normal',
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Endpoints Design (Draft)

### Notifications Routes (~6 endpoints)
```
GET    /api/notifications                    - List user notifications
POST   /api/notifications/mark-read          - Mark notifications as read
DELETE /api/notifications/{id}               - Delete notification
GET    /api/notifications/unread-count       - Get unread count
POST   /api/notifications/mark-all-read      - Mark all as read
GET    /api/notifications/preferences        - Get preferences
PUT    /api/notifications/preferences        - Update preferences
```

### Direct Messages Routes (~5 endpoints)
```
POST   /api/messages/send                    - Send direct message
GET    /api/messages/conversations           - List conversations
GET    /api/messages/conversation/{user_id}  - Get conversation
POST   /api/messages/mark-read               - Mark messages as read
DELETE /api/messages/{id}                    - Delete message
```

### Announcements Routes (~4 endpoints)
```
GET    /api/announcements                    - List announcements
POST   /api/announcements                    - Create announcement (admin)
PUT    /api/announcements/{id}               - Update announcement (admin)
DELETE /api/announcements/{id}               - Delete announcement (admin)
```

---

## Notification Types

### Assignment Notifications
- Assignment created
- Assignment due soon (24h, 1 week)
- Assignment graded
- Assignment overdue

### Goal Notifications
- Goal milestone reached (25%, 50%, 75%)
- Goal completed
- Goal expiring soon
- Goal expired

### Achievement Notifications
- New achievement unlocked
- Level up
- Leaderboard position change

### Social Notifications
- New friend request
- Friend request accepted
- New group invitation
- New group message
- Content shared with you

### Study Notifications
- Study streak maintained
- Study streak broken
- Study goal reminder
- Scheduled study session reminder

---

## Integration Points

### Phase 1 (Classes & Assignments)
- Notify on assignment creation
- Remind about due dates
- Alert on grade updates

### Phase 3 (AI Study Tools)
- Notify when AI notes ready
- Alert when test generated
- Remind to review flashcards

### Phase 4 (Social & Collaboration)
- Friend requests
- Group invitations
- New messages
- Shared content

### Phase 5 (Gamification)
- Achievement unlocked
- Level up
- Leaderboard changes

### Phase 6 (Study Analytics)
- Goal milestones
- Study reminders
- Progress reports ready

---

## Implementation Strategy

### Phase 7.1: Core Notifications (Week 1)
- Database schema
- Basic notification CRUD
- In-app notification display
- Mark as read functionality

### Phase 7.2: Notification Triggers (Week 2)
- Event listeners for all phases
- Automatic notification creation
- Notification preferences
- Batch notifications

### Phase 7.3: Direct Messaging (Week 3)
- Message sending/receiving
- Conversation management
- Real-time updates (WebSocket optional)
- Message notifications

### Phase 7.4: Announcements & Email (Week 4)
- Announcement system
- Email integration (SendGrid/AWS SES)
- Email templates
- Digest emails

---

## Technical Considerations

### Real-time Updates
- **Option 1**: Polling (simple, works everywhere)
- **Option 2**: WebSocket (real-time, more complex)
- **Option 3**: Server-Sent Events (one-way real-time)
- **Recommendation**: Start with polling, add WebSocket later

### Email Service
- **Option 1**: SendGrid (easy, reliable)
- **Option 2**: AWS SES (cost-effective, scalable)
- **Option 3**: SMTP (self-hosted, complex)
- **Recommendation**: AWS SES (already using AWS)

### Push Notifications
- **Option 1**: Firebase Cloud Messaging (cross-platform)
- **Option 2**: AWS SNS (AWS ecosystem)
- **Option 3**: OneSignal (feature-rich)
- **Recommendation**: Defer to mobile app phase

---

## Success Criteria

### Backend
- All notification types triggering correctly
- Preferences respected
- Messages delivered reliably
- Email integration working
- 100% test pass rate

### User Experience
- Notifications appear within 5 seconds
- Unread count updates in real-time
- Email digests sent on schedule
- No notification spam
- Easy to manage preferences

### Performance
- Notification queries < 100ms
- Message delivery < 200ms
- Email queue processing < 1 minute
- Support 1000+ concurrent users

---

## Estimated Timeline

- **Week 1**: Core notifications + database
- **Week 2**: Notification triggers + preferences
- **Week 3**: Direct messaging
- **Week 4**: Announcements + email

**Total**: 4 weeks

---

## Alternative: Phase 7 Options

If notifications aren't the priority, other Phase 7 options:

### Option A: Mobile App Development
- React Native app
- iOS and Android support
- Offline capabilities
- Push notifications

### Option B: Advanced AI Features
- AI study coach
- Personalized recommendations
- Predictive analytics
- Smart scheduling

### Option C: Teacher/Admin Portal
- Class management for teachers
- Student progress monitoring
- Grade management
- Analytics dashboard

### Option D: Payment & Subscriptions
- Stripe integration
- Subscription tiers
- Premium features
- Billing management

---

## Recommendation

**Proceed with Phase 7: Notifications & Communication**

### Rationale
1. Completes the core user engagement loop
2. Leverages all existing phases
3. High user value (keeps users engaged)
4. Moderate complexity (proven patterns)
5. Foundation for mobile app (Phase 8)

---

## Next Steps

1. Review and approve Phase 7 scope
2. Design detailed database schema
3. Create implementation plan
4. Begin development following Phase 6 pattern

---

## Notes

- Phase 6 enhancements documented in PHASE6-BACKLOG.md
- Can return to Phase 6 enhancements anytime
- Phase 7 builds on solid foundation (Phases 1-6)
- Notification system enables future features (mobile, email campaigns)
