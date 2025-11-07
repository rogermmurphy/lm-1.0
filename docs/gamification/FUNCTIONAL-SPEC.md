# Little Monster GPA - Gamification System Functional Specification

## Document Information
- **Version**: 1.0
- **Last Updated**: November 6, 2025
- **Status**: Draft
- **Related Documents**: 
  - `TECHNICAL-SPEC.md`
  - `docs/BUSINESS-PROCESS-FLOWS.md`
  - `services/gamification/README.md`

---

## 1. Executive Summary

The Little Monster GPA gamification system motivates students through a personalized AI-generated monster avatar that evolves as they earn points through study activities. Students customize their monster's appearance and watch it progress through increasingly elaborate AI-generated scenes as their point totals increase.

---

## 2. Core Concept

### 2.1 Monster Avatar System
**Base Monster**: Each user gets a customizable monster character named by the user (e.g., "Dave")

**Physical Characteristics**:
- **Body Type**: Fat/round, friendly appearance
- **Default Color**: Orange
- **Key Feature**: Big hands
- **Personality**: Friendly, encouraging, cute

### 2.2 Customization Options
Users can personalize their monster with:
- **Accessories**: Glasses, hats, scarves
- **Clothing**: T-shirts, dresses, jackets, formal wear
- **Features**: Claws, wings, horns, tail variations
- **Colors**: Different body colors, pattern overlays

### 2.3 Progressive Scene Generation
As students earn points, their monster appears in increasingly impressive AI-generated scenes:

**Point Milestones**:
- **0-100 points**: Simple bedroom scene
- **101-500 points**: Study room with books
- **501-1000 points**: Library setting
- **1001-2500 points**: Classroom teaching other monsters
- **2501-5000 points**: University campus
- **5001-10000 points**: Graduation ceremony
- **10001+ points**: Academic achievement hall of fame

---

## 3. Point System

### 3.1 Point-Earning Activities

**Study Activities**:
- Complete a flashcard session: 10 points
- Generate study notes from material: 15 points
- Take a practice test: 25 points
- Upload new course material: 20 points
- Transcribe a lecture: 30 points

**Engagement Activities**:
- Log in daily: 5 points
- Study session 30+ minutes: 20 points
- Study session 60+ minutes: 40 points
- Complete weekly study goal: 100 points

**Social/Collaboration**:
- Share study materials: 15 points
- Join a study group: 10 points
- Help another student (verified): 50 points

**AI Interaction**:
- Ask 10 AI questions: 10 points
- Use TTS feature: 5 points
- Use STT feature: 5 points

### 3.2 Point Multipliers
- **Streak bonus**: +10% per consecutive day (max 50%)
- **Perfect week**: Complete all tasks 7 days straight = 2x points
- **Study party**: Group study sessions = 1.5x points for all participants

---

## 4. User Experience Flow

### 4.1 Initial Setup
1. User completes registration
2. System generates default orange monster avatar
3. User prompted to:
   - Name their monster
   - Select 3 initial customizations (from limited free options)
   - View intro animation of monster in simple scene

### 4.2 Daily Interaction
1. User logs in → sees current monster in current scene
2. Monster displays:
   - Current point total
   - Progress to next milestone
   - Today's earned points
   - Active streak
3. After earning points → brief animation showing points added
4. Reaching milestone → special animation + scene upgrade reveal

### 4.3 Customization Shop
**Free Items** (always available):
- 5 basic accessories
- 3 clothing options
- 2 feature add-ons

**Unlockable Items** (earned with points):
- Spend 100 points: Unlock premium accessory
- Spend 250 points: Unlock special clothing
- Spend 500 points: Unlock rare features
- Spend 1000 points: Custom color option

**Special Items** (achievement-based):
- Complete 100 flashcards: "Scholar Glasses"
- Reach 30-day streak: "Dedication Crown"
- Help 10 students: "Helper Halo"

### 4.4 Scene Generation Process
1. User reaches point milestone
2. System triggers AI scene generation:
   - Inputs: Monster customizations, point level, user name
   - AI generates scene appropriate to milestone
   - Monster placed in scene with earned items visible
3. User receives notification of upgrade
4. New scene becomes dashboard background/display

---

## 5. Display Integration

### 5.1 Dashboard Integration
**Location**: Bottom right corner of dashboard

**Display Elements**:
- Monster avatar (200x200px)
- Current scene (compressed as background)
- Point counter
- Progress bar to next milestone
- Quick customization button

**Interactions**:
- Click monster → Open full customization modal
- Click points → View detailed point history
- Click progress bar → See next milestone details

### 5.2 Mobile Optimization
- Monster avatar scales to 100x100px on mobile
- Tap to expand to full-screen view
- Swipe through customization options
- Scene loads at lower resolution for performance

---

## 6. AI Image Generation Requirements

### 6.1 Image Generation Specifications
**Image Size**: 1024x1024px for desktop, 512x512px for mobile
**Style**: Cartoon/illustrated, friendly, educational
**Consistency**: Monster must maintain recognizable features across scenes
**Generation Time**: <30 seconds per scene
**Storage**: Generated images cached for reuse

### 6.2 Prompt Structure
```
A friendly [COLOR] cartoon monster named [NAME] with big hands, 
wearing [CUSTOMIZATIONS], in a [SCENE DESCRIPTION].
The monster should look encouraging and cute, suitable for an 
educational app. Art style: modern illustration, vibrant colors.
```

### 6.3 Fallback Strategy
If AI generation fails:
- Use pre-rendered template scenes
- Overlay customizations as separate layers
- Display simplified version until AI available

---

## 7. Leaderboards

### 7.1 Leaderboard Types
**Global Leaderboard**:
- Top 100 point earners (all time)
- Top 50 this week
- Top 25 this month

**Class Leaderboards**:
- Top students per registered class
- Resets each semester

**Friend Leaderboards**:
- Compare with connected friends
- Private, opt-in only

### 7.2 Privacy Controls
- Users can opt out of global leaderboards
- Display name vs real name option
- Monster avatar shown instead of profile pic

---

## 8. Achievements System

### 8.1 Achievement Categories

**Study Achievements**:
- "Flashcard Master": Complete 1000 flashcards
- "Note Taker": Generate 100 study notes
- "Test Champion": Score 90%+ on 50 practice tests

**Consistency Achievements**:
- "Week Warrior": 7-day study streak
- "Month Master": 30-day study streak
- "Semester Star": 120-day study streak

**Social Achievements**:
- "Team Player": Join 5 study groups
- "Helper Hero": Assist 25 students
- "Share Bear": Share 50 study materials

**Monster Achievements**:
- "Fashionista": Unlock 50 customization items
- "Scene Collector": Reach all milestone scenes
- "Perfect Match": Create a 5-star rated monster design

### 8.2 Achievement Display
- Badge icon in dashboard
- Achievement showcase in profile
- Special monster items for major achievements
- Shareable achievement cards for social media

---

## 9. Social Features

### 9.1 Monster Showcase
- Users can make their monster public
- Browse other users' monsters for inspiration
- Like/favorite other monsters
- Copy customization ideas (with attribution)

### 9.2 Monster Battles (Future Feature)
- Study quiz competitions between monsters
- Winner earns bonus points
- Friendly competition, educational focus

---

## 10. Monetization (Future Consideration)

### 10.1 Premium Features
**Monster Plus** ($4.99/month):
- Unlimited customization unlocks
- Priority AI scene generation
- Exclusive premium items
- Custom scene requests
- Multiple monster slots

### 10.2 One-Time Purchases
- Special holiday-themed items
- Collabor ation items (university mascots)
- Custom color palettes

---

## 11. Technical Requirements Summary

**Performance**:
- Point updates: Real-time (<1 second)
- Scene generation: <30 seconds
- Dashboard load with monster: <2 seconds
- Customization changes: Instant preview

**Storage**:
- Monster config: <5KB per user
- Generated scenes: ~500KB per scene (6-8 scenes per user)
- Achievement data: <10KB per user

**Scalability**:
- Support 100K concurrent users
- Handle 1M scene generation requests/day
- Queue system for AI generation during peak times

---

## 12. Future Enhancements

### 12.1 Planned Features
- Monster personality traits based on study patterns
- Animated monster reactions to study milestones
- Monster companions (unlock at very high point levels)
- Seasonal events with special themed items
- Monster trading cards

### 12.2 Integration Opportunities
- University branding partnerships
- Study material provider collaborations
- Educational game developers
- Social media sharing optimization

---

## 13. Success Metrics

### 13.1 Engagement Metrics
- Daily active users with monsters: Target 70%+
- Average customization changes per user: Target 5/week
- Scene milestone completion rate: Target 60% reach 2nd milestone
- Social sharing rate: Target 20% share achievements

### 13.2 Business Metrics
- User retention improvement: Target +30%
- Study session length increase: Target +25%
- Premium conversion rate: Target 15% of active users
- User satisfaction score: Target 4.5/5 stars

---

## 14. User Stories

### 14.1 New User
"As a new student, I want to create a unique monster that represents me, so I feel personally connected to my study progress."

### 14.2 Active Studier
"As an active studier, I want to see my monster evolve and appear in cooler scenes, so I stay motivated to keep studying."

### 14.3 Competitive User
"As a competitive student, I want to compare my monster's progress with friends, so we can motivate each other."

### 14.4 Creative User
"As a creative person, I want lots of customization options, so my monster feels unique and expresses my personality."

---

## 15. Accessibility Considerations

- Colorblind-friendly color palettes
- Text alternatives for all visual elements
- Keyboard navigation for customization
- Screen reader support for point announcements
- Option to disable animations for users with motion sensitivity

---

## 16. Content Moderation

### 16.1 Customization Guidelines
- No inappropriate combinations flagged by AI
- No offensive names or text
- Report system for inappropriate public monsters
- Automated filtering of generated scenes

### 16.2 Safe AI Generation
- Content safety filters on all AI-generated images
- Review queue for flagged content
- Age-appropriate themes only
- Educational context maintained

---

## Approval & Sign-off

**Product Owner**: ___________________ Date: ___________

**Development Lead**: ___________________ Date: ___________

**UX Designer**: ___________________ Date: ___________
